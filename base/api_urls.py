from django.urls import path
from . import api_views

urlpatterns = [
    path('test/', api_views.test, name='test'),
]
