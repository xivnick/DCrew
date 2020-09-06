from django.shortcuts import render, redirect
from room.models import Room, RoomUser
from .models import Game
from game.forms import CreateGameForm

from dcrew.settings import SOCKET_URL
import requests


# Create your views here.
def game_create(req, room):

    if req.method == 'POST':
        create_game_form = CreateGameForm(req.POST)

        if create_game_form.is_valid():

            game_instance = create_game_form.save(commit=False)

            game_instance.stage = req.POST['stage']

            game_instance.playerNum = 3

            room_users = RoomUser.objects.filter(room__id=room.id, seat__isnull=False)

            # for ru in room_users:
            #

            game_instance.save()

            Room.objects.filter(id=room.id).update(game=game_instance)

            if game_instance is not None:

                requests.post(SOCKET_URL + '/rooms/update', data={
                    'rooms': [0, room.id],
                    'target': 'forward',
                })

                return redirect('room', room_id=room.id)

    create_game_form = CreateGameForm()

    return render(req, 'game/room.html', {'room': room, 'form': create_game_form})


def game(req, room, room_users):

    my_seat = None
    for ru in room_users:
        if ru.user_id == req.user.id:
            my_seat = ru.seat
            break

    game = Game.objects.filter(id=room.game.id)[0]

    return render(req, 'game/game.html', {'game': game, 'room': room, 'my_seat': my_seat})
