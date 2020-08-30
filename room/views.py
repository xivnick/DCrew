from django.shortcuts import render, redirect
from django.db.models import Subquery, OuterRef, Count
from .models import Room, RoomUser
from .forms import CreateRoomForm
from game.forms import CreateGameForm

from dcrew.settings import SOCKET_URL
import requests


# Create your views here.
def room_list(req):

    return render(req, 'room/list.html')


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

            # 방이 제대로 만들어졌다면
            if room_instance is not None:
                return redirect('room', room_id=room_instance.id)

    else:
        create_room_form = CreateRoomForm()

    return render(req, 'room/create.html', {'form': create_room_form})


def room(req, room_id):

    # get data
    room = Room.objects.filter(id=room_id)[0]
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
            room_seats = (ru.seat for ru in room_users if ru.seat > 0)
            for seat in range(1, room.capacity + 1):
                if seat not in room_seats:
                    room_user.seat = seat
                    break

        # save room player
        room_user.save()

        requests.post(SOCKET_URL + '/game/update', data={
            'room': 0,
            'target': 'all'
        })

    create_game_form = CreateGameForm()

    return render(req, 'room/room.html', {'room': room, 'form': create_game_form})
