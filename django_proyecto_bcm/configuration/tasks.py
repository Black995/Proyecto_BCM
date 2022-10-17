from celery import shared_task

from configuration.models import ProductActivation


@shared_task()
def ExpirationDateVerification():
    ProductActivation.ExpirationDateVerification()