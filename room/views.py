from django.shortcuts import render, redirect
from django.db.models import Subquery, OuterRef
from .models import Room
from django.contrib.auth.models import User
from .forms import CreateRoomForm


# Create your views here.
def room_list(req):

    # 방 목록 가져오기 / 게임 중인 방은 아래
    host_name = User.objects.filter(id=1).values('first_name')[:1]
    rooms = Room.objects.all().annotate(host_name=Subquery(host_name)).order_by('-status')

    if len(rooms) > 0:
        return render(req, 'room/list.html', {'rooms': rooms})

    else:
        return render(req, 'room/list.html', {'empty': True})


def room_create(req):

    if req.method == 'POST':
        create_room_form = CreateRoomForm(req.POST)

        if create_room_form.is_valid():
            room_instance = create_room_form.save(commit=False)

            room_instance.hostId = req.user.id

            rooms = Room.objects.all().values('id').order_by('id')

            new_id = 1
            for room in rooms:
                if room['id'] == new_id:
                    new_id += 1
                else:
                    break

            room_instance.id = new_id

            room_instance.save()

            # 방이 제대로 만들어졌다면
            return redirect('room_list')

    else:
        create_room_form = CreateRoomForm()

    return render(req, 'room/create.html', {'form': create_room_form})
