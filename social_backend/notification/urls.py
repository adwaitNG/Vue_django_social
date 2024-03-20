from django.urls import path

from . import api
urlpatterns = [
    path('', api.notifications, name="notifications"),
    path('read/<uuid:id>/', api.readNotificationRequest, name="read_notifications")
]