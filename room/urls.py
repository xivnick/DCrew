from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.room_list, name='room_list'),
    path('create/', views.room_create, name='room_create'),
    path('<int:room_id>/', views.room, name='room'),
    path('<int:room_id>/exit/', views.room_exit, name='room_exit'),
    path('<int:room_id>/end_game/', views.room_end_game, name='room_end_game'),
]
