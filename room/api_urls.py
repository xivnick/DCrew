from django.urls import path
from . import api_views

urlpatterns = [
    path('list/', api_views.room_list, name='api_room_list'),
    path('user/update/', api_views.room_user_update, name='api_room_user_update'),
]
