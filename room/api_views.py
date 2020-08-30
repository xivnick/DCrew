from django.db.models import Subquery, OuterRef, Count
from .models import Room, RoomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dcrew.settings import get_secret
import json


@csrf_exempt
def room_user_update(req):

    if req.method == 'POST':
        data = json.loads(req.body)

        # check x_key
        if 'x_key' not in data or data['x_key'] != get_secret('X_KEY'):
            return JsonResponse({}, status=403)

        # check params
        params = ['type', 'room_id', 'user_id']
        for param in params:
            if param not in data:
                return JsonResponse({'message': 'need param \''+param+'\''}, status=422)

        result = RoomUser.objects.filter(room__id=data['room_id'], user__id=data['user_id']).update(
            connect=(data['type'] == 'connect')
        )

        if result == 0:
            return JsonResponse({'message': 'no room user'}, status=400)

        return JsonResponse({'message': 'success', 'result': result})

    return JsonResponse(status=404)
