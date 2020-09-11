from django.urls import path
from . import api_views

urlpatterns = [
    path('misson/', api_views.mission, name='api_game_mission'),
]
