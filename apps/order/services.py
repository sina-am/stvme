from apps.order import queryset
from apps.order import models
from apps.payment.models import Invoice
from django.db import transaction
import datetime


def offer_to_translator(order_id: int):
    translators = queryset.find_best_match(order_id, None)
    offer_list = []
    for translator_id in translators.values_list('pk', flat=True):
        offer_list.append(
            models.OrderOffer(order_id=order_id,translator_id=translator_id, price=0)
        )
        
    models.OrderOffer.objects.bulk_create(offer_list)

