from django.shortcuts import resolve_url
from django.db.models import Subquery, OuterRef, Count
from .models import Room, RoomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dcrew.settings import get_secret
import json

from dcrew.settings import SOCKET_URL
import requests


def room_list(req):

    # 방 목록 가져오기 / 게임 중인 방은 아래
    room_player_num = RoomUser.objects.filter(
        room__id=OuterRef('id'), seat__isnull=False
    ).values('room__id').annotate(playerNum=Count('room__id')).values('playerNum')
    rooms = Room.objects.select_related('host').annotate(
        playerNum=Subquery(room_player_num)
    ).order_by('game__id')

    rooms = [{
        'id': room.id,
        'title': room.title,
        'capacity': room.capacity,
        'host_name': room.host.first_name,
        'game_id': room.game_id,
        'player_num': room.playerNum or 0,
        'room_url': resolve_url('room', room_id=room.id),
    } for room in rooms]

    return JsonResponse({'rooms': rooms})


def room_my_rooms(req):

    params = ['user_id']
    for param in params:
        if param not in req.GET:
            return JsonResponse({'message': 'need param \'' + param + '\''}, status=422)

    user_id = req.GET['user_id']

    room_users = RoomUser.objects.filter(user_id=user_id)

    rooms = [ru.room_id for ru in room_users]

    return JsonResponse({'rooms': rooms})


def room_users(req):

    params = ['room_id']
    for param in params:
        if param not in req.GET:
            return JsonResponse({'message': 'need param \'' + param + '\''}, status=422)

    room_id = req.GET['room_id']

    room_users = RoomUser.objects.filter(room__id=room_id)

    my_seat = None
    for ru in room_users:
        if ru.user_id == req.user.id:
            my_seat = ru.seat
            break

    room_users = [{
        'user_id': ru.user_id,
        'name': ru.user.first_name,
        'seat': ru.seat,
        'connect': ru.connect,
    } for ru in room_users]

    return JsonResponse({'room_users': room_users, 'my_seat': my_seat})


def room_user_delete(req):

    if req.method == 'POST':
        data = json.loads(req.body)

        # check params
        params = ['room_id', 'user_id']
        for param in params:
            if param not in data:
                return JsonResponse({'message': 'need param \'' + param + '\''}, status=422)

        room_id = data['room_id']
        user_id = data['user_id']

        # check host
        room = Room.objects.filter(id=room_id)[0]
        if room.host != req.user:
            return JsonResponse({'message': 'you\'re not a host'}, status=403)

        result = RoomUser.objects.filter(room__id=room_id, user__id=user_id).delete()

        requests.post(SOCKET_URL + '/rooms/update', data={
            'rooms': [room_id, 0],
            'target': 'all'
        })

        return JsonResponse({'message': 'success', 'result': result})

    return JsonResponse({}, status=404)


@csrf_exempt
def room_user_update(req):

    if req.method == 'POST':
        data = json.loads(req.body)

        # check x_key
        if 'x_key' not in data or data['x_key'] != get_secret('X_KEY'):
            return JsonResponse({}, status=403)

        # check params
        params = ['type', 'room_id', 'user_id']
        for param in params:
            if param not in data:
                return JsonResponse({'message': 'need param \''+param+'\''}, status=422)

        result = RoomUser.objects.filter(room__id=data['room_id'], user__id=data['user_id']).update(
            connect=(data['type'] == 'connect')
        )

        if result == 0:
            return JsonResponse({'message': 'no room user'}, status=400)

        requests.post(SOCKET_URL + '/room/update', data={
            'room': data['room_id'],
            'target': 'all'
        })

        return JsonResponse({'message': 'success', 'result': result})

    return JsonResponse({}, status=404)


def room_user_seat_update(req):

    if req.method == 'POST':
        data = json.loads(req.body)

        # check params
        params = ['room_id', 'user_id', 'seat']
        for param in params:
            if param not in data:
                return JsonResponse({'message': 'need param \'' + param + '\''}, status=422)

        # check user in room
        result = RoomUser.objects.filter(room__id=data['room_id'], user__id=data['user_id']).update(
            seat=data['seat']
        )

        requests.post(SOCKET_URL + '/rooms/update', data={
            'rooms': [data['room_id'], 0],
            'target': 'all'
        })

        return JsonResponse({'message': 'success', 'result': result})

    return JsonResponse({}, status=404)
