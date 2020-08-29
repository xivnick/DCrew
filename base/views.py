from django.shortcuts import render, redirect
from .models import Notice
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dcrew.settings import get_secret
import json


# Create your views here.
def root(req):
    print(req.user)
    if req.user.is_anonymous:
        return redirect('account_login')

    return redirect('room_list')


def base(req):
    return render(req, 'base/base.html')


def notice(req):

    try:
        text = Notice.objects.all().order_by('-id').values('text')[:1][0]['text']

    except IndexError:
        text = ''

    print(text)

    return render(req, 'base/notice.html', {'notice': text})


@csrf_exempt
def test(req):

    data = json.loads(req.body)

    # check x_key
    if 'x_key' not in data or data['x_key'] != get_secret('X_KEY'):
        return JsonResponse({}, status=403)

    print('data: ', data)
    return JsonResponse({'message': 'success'})
