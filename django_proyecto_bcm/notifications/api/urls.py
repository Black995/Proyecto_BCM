from django.urls import path
from .views import (NotificacionListCreate, unread_notifications)


urlpatterns = [
    path("/", NotificacionListCreate.as_view({
        'get': 'list',
        'post': 'create'
        }), name="notification_list"),
    path("unread_notifications/", unread_notifications.as_view({
        'get': 'list',
        }), name="unread_notifications"),
]
