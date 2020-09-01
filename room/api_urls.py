from django.urls import path
from . import api_views

urlpatterns = [
    path('list/', api_views.room_list, name='api_room_list'),
    path('user/update/', api_views.room_user_update, name='api_room_user_update'),
    path('users/', api_views.room_users, name='api_room_users'),
    path('my_rooms', api_views.room_my_rooms, name='api_room_my_rooms')
]
