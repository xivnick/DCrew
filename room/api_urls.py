from django.urls import path
from . import api_views

urlpatterns = [
    path('user/update/', api_views.room_user_update, name='api_room_user_update'),
]