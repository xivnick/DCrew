from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dcrew.settings import get_secret
import json


@csrf_exempt
def test(req):

    data = json.loads(req.body)

    # check x_key
    if 'x_key' not in data or data['x_key'] != get_secret('X_KEY'):
        return JsonResponse({}, status=403)

    print('data: ', data)
    return JsonResponse({'message': 'success'})
