from layout.models import Risk
from django.shortcuts import get_object_or_404
from .serializers import RiskSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class RiskViewSet(viewsets.ModelViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer


# Ejemplo de ViewSet (no de ModelViewSet)
"""
class RiskViewSet(viewsets.ViewSet):
    model = Risk
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer

    def list(self, request):
        queryset = Risk.objects.all()
        serializer = RiskSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, serializer):
        serializer.save()
"""
