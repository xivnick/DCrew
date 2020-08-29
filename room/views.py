from django.shortcuts import render, redirect
from django.db.models import Subquery, OuterRef, Count
from .models import Room, RoomUser
from django.contrib.auth.models import User
from .forms import CreateRoomForm
from game.forms import CreateGameForm


# Create your views here.
def room_list(req):

    # 방 목록 가져오기 / 게임 중인 방은 아래
    host_name = User.objects.filter(id=OuterRef('hostId')).values('first_name')
    rooms = Room.objects.all().annotate(hostName=Subquery(host_name)).order_by('gameId').values()

    room_player_nums = RoomUser.objects.filter(seat__gt=0).values('roomId').annotate(playerNum=Count('roomId'))

    room_player_nums = {rpn['roomId']: rpn['playerNum'] for rpn in room_player_nums}
    rooms = [{
        **room,
        'playerNum': room_player_nums[room['id']] if room['id'] in room_player_nums else 0,
    } for room in rooms]

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
            room_instance.host_id = req.user.id

            # save room
            room_instance.save()

            # make room player
            room_player = RoomUser()
            room_player.roomId = room_instance.id
            room_player.userId = req.user.id
            room_player.seat = 1

            # save room player
            room_player.save()

            # 방이 제대로 만들어졌다면
            return redirect('room_list')

    else:
        create_room_form = CreateRoomForm()

    return render(req, 'room/create.html', {'form': create_room_form})


def room(req, room_id):

    # get data
    room = Room.objects.filter(id=room_id).values()[0]
    room_users = RoomUser.objects.filter(roomId=room_id).values()

    # check user in room
    user_id = req.user.id
    room_user_ids = (ru['userId'] for ru in room_users)

    if user_id not in room_user_ids:
        # push user into room

        # make room player
        room_user = RoomUser()
        room_user.roomId = room_id
        room_user.userId = user_id

        # if waiting, get smallest seat
        if room['gameId'] is None:
            room_seats = (ru['seat'] for ru in room_users if ru['seat'] > 0)
            for seat in range(1, room['capacity'] + 1):
                if seat not in room_seats:
                    room_user.seat = seat
                    break

        # save room player
        room_user.save()

    create_game_form = CreateGameForm()

    return render(req, 'room/room.html', {'room': room, 'form': create_game_form})
