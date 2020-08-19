from django.urls import path
from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('base/', views.base, name='base'),
]