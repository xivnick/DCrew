from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.room_list, name='room_list'),
    path('create/', views.room_create, name='room_create'),
    path('user/', views.room_user, name='room_user'),
    path('<int:room_id>/', views.room, name='room'),
]
