from django.shortcuts import render, redirect
from .models import Notice


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

    return render(req, 'base/notice.html', {'notice': text})
