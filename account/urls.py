from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='account_login'),
    path('logout/', views.logout, name='account_logout'),
    path('signup/', views.signup, name='account_signup'),
]

