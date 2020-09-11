from .missions import missions
from django.http import JsonResponse
import json


def mission(req):

    params = ['stage']
    for param in params:
        if param not in req.GET:
            return JsonResponse({'message': 'need param \'' + param + '\''}, status=422)

    stage = int(req.GET['stage'])

    mission = missions[stage]

    return JsonResponse({'mission': mission})
