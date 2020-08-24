from django.shortcuts import render, redirect
from django.db.models import Subquery, OuterRef, Count
from .models import Room, RoomUser
from django.contrib.auth.models import User
from .forms import CreateRoomForm


# Create your views here.
def room_list(req):

    # 방 목록 가져오기 / 게임 중인 방은 아래
    rooms = Room.objects.all().order_by('-status').values()

    host_name = User.objects.filter(id=OuterRef('userId')).values('first_name')
    room_host_names = RoomUser.objects.filter(type='H').annotate(
        hostName=Subquery(host_name)
    ).values('roomId', 'hostName')
    room_player_nums = RoomUser.objects.all().values('roomId').annotate(playerNum=Count('roomId'))

    room_host_names = {rhn['roomId']: rhn['hostName'] for rhn in room_host_names}
    room_player_nums = {rpn['roomId']: rpn['playerNum'] for rpn in room_player_nums}
    rooms = [{
        **room,
        'host_name': room_host_names[room['id']],
        'player_num': room_player_nums[room['id']],
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

            # save room
            room_instance.save()

            # make room player
            room_player = RoomUser()
            room_player.roomId = room_instance.id
            room_player.userId = req.user.id
            room_player.type = 'H'

            # save room player
            room_player.save()

            # 방이 제대로 만들어졌다면
            return redirect('room_list')

    else:
        create_room_form = CreateRoomForm()

    return render(req, 'room/create.html', {'form': create_room_form})
