from django.shortcuts import render, redirect
from django.db.models import Subquery, OuterRef, Count
from .models import Room, RoomUser
from .forms import CreateRoomForm
from game.forms import CreateGameForm

from dcrew.settings import SOCKET_URL
import requests

from account.views import login_redirect


# Create your views here.
def room_list(req):

    return render(req, 'room/list.html')


def room_create(req):

    if req.user.is_anonymous:
        return login_redirect('room_create')

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

            # 방이 제대로 만들어졌다면
            if room_instance is not None:
                return redirect('room', room_id=room_instance.id)

    else:
        create_room_form = CreateRoomForm()

    return render(req, 'room/create.html', {'form': create_room_form})


def room_exit(req, room_id):
    if req.user.is_anonymous:
        return redirect('room_list')

    rooms = Room.objects.filter(id=room_id)
    if len(rooms):
        room = rooms[0]

        if room.host == req.user:
            room.delete()

            requests.post(SOCKET_URL + '/room/delete', data={
                'room': room_id,
            })

        else:
            room_users = RoomUser.objects.filter(room__id=room_id, user__id=req.user.id)
            if len(room_users):
                room_user = room_users[0]
                room_user.delete()

                requests.post(SOCKET_URL + '/room/update', data={
                    'room': room_id,
                    'target': 'all',
                })

    return redirect('room_list')


def room(req, room_id):

    # check user login
    if req.user.is_anonymous:
        return login_redirect('room', room_id=room_id)

    # check there is room with roomid
    rooms = Room.objects.filter(id=room_id)
    if len(rooms) == 0: return redirect('room_list')

    # get room data
    room = rooms[0]
    room_users = RoomUser.objects.filter(room__id=room_id)

    # check user in room
    if req.user.id not in (ru.user.id for ru in room_users):
        # push user into room

        # make room player
        room_user = RoomUser()
        room_user.room = room
        room_user.user = req.user

        # if waiting, get smallest seat
        if room.game is None:
            room_seats = (ru.seat for ru in room_users if ru.seat is not None)
            print(*room_seats)
            for seat in range(1, room.capacity + 1):
                if seat not in room_seats:
                    print('seat:', seat)
                    room_user.seat = seat
                    break

        # save room player
        room_user.save()

        requests.post(SOCKET_URL + '/room/update', data={
            'room': 0,
            'target': 'all',
        })

    create_game_form = CreateGameForm()

    return render(req, 'room/room.html', {'room': room, 'form': create_game_form})
