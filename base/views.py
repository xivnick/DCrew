from django.shortcuts import render, redirect


# Create your views here.
def root(req):
    print(req.user)
    if req.user.is_anonymous:
        return redirect('account_login')

    return redirect('room_list')


def base(req):
    return render(req, 'base/base.html')
