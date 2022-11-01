from bcm_phase1.models import Risk, CrisisScenario
from django.http.response import Http404
from django.shortcuts import HttpResponse, get_object_or_404
from .serializers import (RiskSerializer, CrisisScenarioSerializer, CrisisScenarioListSerializer,
                            ServicesOfferedRiskListSerializer)
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q, F
from rest_framework.views import APIView
from django.conf import settings
import os


class RiskViewSet(viewsets.ModelViewSet):
    model = Risk
    queryset = Risk.objects.all().order_by('name')
    serializer_class = RiskSerializer


class CrisisScenarioViewSet(viewsets.ModelViewSet):
    model = CrisisScenario
    queryset = CrisisScenario.objects.all()
    serializer_class = CrisisScenarioSerializer


class CrisisScenarioListViewSet(viewsets.ModelViewSet):
    model = CrisisScenario
    queryset = CrisisScenario.objects.all().order_by('name')
    serializer_class = CrisisScenarioListSerializer

class CrisisScenarioListRisksViewSet(viewsets.ModelViewSet):
    model = CrisisScenario
    queryset = CrisisScenario.objects.all()
    serializer_class = CrisisScenarioSerializer


class ServicesOfferedRiskListViewSet(viewsets.ModelViewSet):
    model = Risk
    queryset = Risk.objects.all().order_by('name')
    serializer_class = ServicesOfferedRiskListSerializer


class DownloadCrisisScenarioDocument(APIView):
    queryset = CrisisScenario.objects.all()

    def get(elf, request, id):
        crisis = get_object_or_404(CrisisScenario, id=id)
        file_path = os.path.join(
            settings.STATICFILES_DIRS[3], str(crisis.documentation))
        if(crisis.documentation):
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="multipart/form-data")
                    response['Content-Disposition'] = 'inline; filename=' + \
                        os.path.basename(file_path)
                    return response
            raise Http404
        # raise Http404
        return Response({"menssage": "this crisis scenario does not have documentation yet"}, status=status.HTTP_400_BAD_REQUEST)
