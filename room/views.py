from django.shortcuts import render, redirect, reverse
from django.db.models import Subquery, OuterRef, Count
from .models import Room, RoomUser
from django.contrib.auth.models import User
from .forms import CreateRoomForm
from game.forms import CreateGameForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dcrew.settings import get_secret
import json


# Create your views here.
def room_list(req):

    # 방 목록 가져오기 / 게임 중인 방은 아래
    room_player_num = RoomUser.objects.filter(
        seat__gt=0, room__id=OuterRef('id')
    ).values('room__id').annotate(playerNum=Count('room__id')).values('playerNum')
    rooms = Room.objects.select_related('host').annotate(playerNum=Subquery(room_player_num)).order_by('game__id')

    if len(rooms) > 0:
        return render(req, 'room/list.html', {'rooms': rooms})

    else:
        return render(req, 'room/list.html', {'empty': True})


def room_create(req):

    if req.method == 'POST':
        create_room_form = CreateRoomForm(req.POST)

        if create_room_form.is_valid():
            room_instance = create_room_form.save(commit=False)

            # find empty room id
            rooms = Room.objects.all().values('id').order_by('id')

            new_id = 1
            for room in rooms:
                if room['id'] == new_id:
                    new_id += 1
                else:
                    break

            room_instance.id = new_id
            room_instance.host = req.user

            # save room
            room_instance.save()

            if room_instance is not None:
                # 방이 제대로 만들어졌다면
                return redirect('room', room_id=room_instance.id)

    else:
        create_room_form = CreateRoomForm()

    return render(req, 'room/create.html', {'form': create_room_form})


@csrf_exempt
def room_user_update(req):

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

    return JsonResponse({'message': 'success', 'result': result})


def room(req, room_id):

    # get data
    room = Room.objects.filter(id=room_id)[0]
    room_users = RoomUser.objects.filter(room__id=room_id)

    print(room)

    # check user in room
    if req.user.id not in (ru.user.id for ru in room_users):
        # push user into room

        # make room player
        room_user = RoomUser()
        room_user.room = room
        room_user.user = req.user

        # if waiting, get smallest seat
        if room.game is None:
            room_seats = (ru.seat for ru in room_users if ru.seat > 0)
            for seat in range(1, room.capacity + 1):
                if seat not in room_seats:
                    room_user.seat = seat
                    break

        # save room player
        room_user.save()

    create_game_form = CreateGameForm()

    return render(req, 'room/room.html', {'room': room, 'form': create_game_form})
