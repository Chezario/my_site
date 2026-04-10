from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('form/', views.my_form_view, name='my_form'),
]
