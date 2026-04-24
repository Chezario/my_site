from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('form/', views.my_form_view, name='my_form'),
    path('<int:operation_id>/', views.operation_details, name='details'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

handler404 = 'pages.views.custom_404'