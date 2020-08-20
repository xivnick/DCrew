from django.shortcuts import render
from django.db.models import Subquery, OuterRef
from .models import Room
from django.contrib.auth.models import User


# Create your views here.
def room_list(req):

    # 방 목록 가져오기 / 게임 중인 방은 아래
    host_name = User.objects.filter(id=1).values('first_name')[:1]
    rooms = Room.objects.all().annotate(host_name=Subquery(host_name)).order_by('-status')

    if len(rooms) > 0:
        return render(req, 'room/room_list.html', {'rooms': rooms})

    else:
        return render(req, 'room/room_list.html', {'empty': True})
