from celery import shared_task

from notifications.models import Notification


@shared_task()
def RemainingActivationTimeNotifiaction():
    Notification.RemainingActivationTimeNotifiaction()
    