from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.index, name='index'),
]
