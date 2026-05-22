from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'vpn'

urlpatterns = [
    path("", views.vpn_users_page, name='vpn_users_page'),
    path(
        "api/create/",
        views.create_vpn_user,
        name="create_vpn_user"
    ),
    # path(
    #     "api/list/",
    #     views.list_vpn_users,
    #     name="list_vpn_users"
    # ),
    path(
        "api/delete/<str:username>",
        views.delete_vpn_user,
        name="delete_vpn_user"
    ),
    path(
        "download/<str:username>/",
        views.download_config,
        name="download_config"
    ),
    path(
        "download_qr/<str:username>/",
        views.download_qr,
        name="download_qr"
    ),
]

handler404 = 'pages.views.custom_404'