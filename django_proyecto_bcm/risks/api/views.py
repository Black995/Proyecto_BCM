from layout.models import Risk, CrisisScenario
from django.shortcuts import get_object_or_404
from .serializers import RiskSerializer, CrisisScenarioSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q, F


class RiskViewSet(viewsets.ModelViewSet):
    model = Risk
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer


class CrisisScenarioViewSet(viewsets.ViewSet):
    model = CrisisScenario
    serializer_class = CrisisScenarioSerializer
    queryset = CrisisScenario.objects.all()
    # queryset = CrisisScenario.objects.annotate(risks_name=F('risks__name'))

    def list(self, request):
        queryset = CrisisScenario.objects.all()
        serializer = CrisisScenario(queryset, many=True)
        return Response(serializer.data)

    def create(self, serializer):
        serializer.save()

    """
    def create(self, serializer):
        id_risks = self.request.GET.get('risks')
        print(id_risks)
        crisisScenario = serializer
        # crisisScenario = serializer.save()
        for id in id_risks:
            print(id)
            risk = Risk.objects.get(id=id)
            crisisScenario.risks.add(risk)
        crisisScenario.save()
    """


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
