from django.contrib import admin
from django.urls import path

import main.views

urlpatterns = [
    path('', main.views.index, name="index"),
    path('login', main.views.login_view, name="login"),
    path('logout', main.views.logout_view, name="logout"),
    path('register', main.views.register, name="register"),
    path('main', main.views.main, name="main"),
    path('logs', main.views.logsView, name="logsView"),
    path('access-list', main.views.accessListView, name="accessListView"),

    path('device/add', main.views.addDevice, name="addDevice"),
    path('device/<int:id>', main.views.getDeviceInfo, name="getDeviceInfo"),
    path('device/grant-access', main.views.grantAccess, name="grantAccess"),
    path('device/delete-access', main.views.deleteAccess, name="deleteAccess"),
    path('device/status/<str:identifier>', main.views.getDeviceStatus, name="getDeviceStatus"),
    path('device/set-status', main.views.setDeviceStatus, name="setDeviceStatus"),
    path('device/get-access', main.views.getAccess, name="grantAccess"),
    path('device/<int:device_id>/logs', main.views.getDeviceLogs, name="getDeviceLogs"),
]
