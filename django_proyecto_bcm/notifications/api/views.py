
from notifications.models import Notification, N_U
from .serializers import (NotificationSerializer, N_USerializer)
from django.db.models import Q, F
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import (ListCreateAPIView)
from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import EmailMessage
from bcm_phase1.models import Risk, CrisisScenario
from bcm_phase2.models import ServiceOffered, SO_S
from bcm_phase3.models import IncidentHistory
from users.models import User


class NotificacionListViewSet(viewsets.ModelViewSet):
    queryset = N_U.objects.filter(read=False)
    serializer_class = N_USerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(user=user)
        return queryset


class N_UViewSet(viewsets.ModelViewSet):
    queryset = N_U.objects.all()
    serializer_class = N_USerializer


class unread_notifications(ListCreateAPIView):
    queryset = N_U.objects.all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get(self, request):
        user = request.user
        amount = N_U.objects.filter(user=user, read=False).count()
        return Response(amount)


"""
    Notification list
"""

class IncidentCreatedNotification(APIView):
    queryset = IncidentHistory.objects.all()
    serializer_class = NotificationSerializer

    def post(self, request):
        incident_history_id = self.request.data.get("incident_history_id")

        incident_history = IncidentHistory.objects.get(id=incident_history_id)

        if (incident_history):
            title = "Nueva incidente creado - Sistema BCM"
            description = "Se les informa que ha sido creado un nuevo incidente de \"" + incident_history.crisis_scenario.name + " \", el cual posee un rango de fechas desde el " + incident_history.start_date.strftime("%m/%d/%Y, %H:%M:%S") + " hasta el " + incident_history.end_date.strftime("%m/%d/%Y, %H:%M:%S") + ".\nSe les recomienda entrar en contacto con los supervisores y gerentes de la organización."


            # Query to get all staff affected by incident

            # 1. Relevant staff affected by incident
            risks = CrisisScenario.objects.filter(id=incident_history.crisis_scenario.id).values('_risks')
            risks_id = []
            for r in risks:
                risks_id.append(r['_risks'])
            
            services_offered_id = ServiceOffered.objects.filter(_risks__in=risks_id).distinct().values('id')

            relevant_staff_id = SO_S.objects.filter(service_offered__in=services_offered_id, relevant=True).distinct().values('staff__id')
            relevant_staff_id

            users = User.objects.filter(staff__in=relevant_staff_id)

            # 2. Staff with a relevant position
            user_relevant_by_position = User.objects.filter(staff__isnull=False, staff__position__relevant=True)

            # Save email and id from users
            user_list = []
            email_list = []
            for u in users:
                user_list.append(u)
                email_list.append(u.email)
            
            for u in user_relevant_by_position:
                if not u in user_list:
                    user_list.append(u)
                    email_list.append(u.email)
            """
            email_message = EmailMessage(
                subject=title,
                body=description,
                from_email=settings.EMAIL_HOST_USER,
                bcc=email_list
            )
            email_message.send()
            """

            notif = Notification.objects.create(
                title=title, 
                description=description,
                type=2
            )
            for u in user_list:
                N_U.objects.create(
                    read=False,
                    notification=notif,
                    user=u
                )
            # notif.users.set(user_id_list)
            
            return Response()
