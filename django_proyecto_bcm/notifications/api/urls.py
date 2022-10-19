from django.urls import path
from .views import (NotificacionListViewSet, N_UViewSet, unread_notifications,
                    IncidentCreatedNotification,ModifiedScaleNotification)


urlpatterns = [
    path("notifications/", NotificacionListViewSet.as_view({
        'get': 'list',
        'post': 'create'
        }), name="notification_list"),
    path('notification/<int:pk>/', N_UViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='notification_detail'),
    path("unread_notifications/", unread_notifications.as_view(), name="unread_notifications"),

    # Notification list    
    path("notify_incident_created/", IncidentCreatedNotification.as_view(),
         name="notify_incident_created"),
    path("notify_modified_scale/", ModifiedScaleNotification.as_view(),
         name="notify_modified_scale")
]
