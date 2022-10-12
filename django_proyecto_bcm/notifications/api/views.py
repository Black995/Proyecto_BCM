
from notifications.models import Notification
from .serializers import (NotificationSerializer)
from django.db.models import Q, F
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response


class NotificacionListCreate(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        return serializer.save(usuarios=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(users=user)
        read = self.request.GET.get("read")
        queryset = queryset.filter(read=read) if read else queryset
        return queryset



class unread_notifications(viewsets.ModelViewSet):
    queryset = Notification.objects.all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get(self, request):
        user = request.user
        amount = Notification.objects.filter(
            users=user, read=False).count()
        return Response(amount)
