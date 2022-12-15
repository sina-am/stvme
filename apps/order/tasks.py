from celery import shared_task
from apps.order import queryset
from apps.order import models
from apps.order import services


@shared_task
def offer_to_translator(order_id: int):
    services.offer_to_translator(order_id)


@shared_task
def test():
    ...