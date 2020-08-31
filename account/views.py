from django.shortcuts import render, redirect, reverse, resolve_url
from django.contrib import auth

from .forms import SignUpForm, LoginForm


# Create your views here.
def login(req):
    if not req.user.is_anonymous:
        return redirect('root')

    if req.method == 'POST':
        next = req.POST['next'] if 'next' in req.POST else 'root'
        login_form = LoginForm(req.POST)

        username = req.POST['username']
        password = req.POST['password']
        user = auth.authenticate(req, username=username, password=password)

        if user is not None:
            auth.login(req, user)

            print('[log]', username, 'login')

            return redirect(next)

        return render(req, 'account/login.html', {'form': login_form, 'failed': True, 'next': next})

    next = req.GET['next'] if 'next' in req.GET else 'root'
    login_form = LoginForm()

    return render(req, 'account/login.html', {'form': login_form, 'failed': False, 'next': next})


def logout(req):
    user = req.user
    auth.logout(req)

    print('[log]', user, 'logout')

    return redirect('account_login')


def signup(req):

    if req.method == 'POST':
        next = req.POST['next'] if 'next' in req.POST else 'root'
        signup_form = SignUpForm(req.POST)

        if signup_form.is_valid():

            user_instance = signup_form.save(commit=False)

            user_instance.set_password(signup_form.cleaned_data['password'])
            user_instance.last_name = signup_form.cleaned_data['first_name']

            user_instance.save()

            # 회원가입이 정상적으로 되었을때만
            return redirect(reverse('account_login')+'?next='+next)

    else:
        next = req.GET['next'] if 'next' in req.GET else 'root'
        signup_form = SignUpForm()

    return render(req, 'account/signup.html', {'form': signup_form, 'next': next})


def login_redirect(next, **kwargs):

    url = reverse('account_login') + '?next=' + resolve_url(next, **kwargs)

    return redirect(url)
