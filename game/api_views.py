from .missions import missions
from django.http import JsonResponse
from .models import Game
import json


def game(req):

    params = ['game_id']
    for param in params:
        if param not in req.GET:
            return JsonResponse({'message': 'need param \'' + param + '\''}, status=422)

    game_id = int(req.GET['game_id'])

    game = Game.objects.filter(id=game_id)[0]

    game = {
        'id': game.id,
        'mode': game.mode,
        'stage': game.stage,
        'mission': missions[game.stage]
    }

    return JsonResponse({'game': game})
