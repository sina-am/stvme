from apps.order import queryset
from apps.order import models
from apps.payment.models import Invoice
from django.db import transaction
import datetime


def offer_to_employee(order_id: int):
    employees = queryset.find_best_match(order_id, None)
    offer_list = []
    for employee_id in employees.values_list('pk', flat=True):
        offer_list.append(
            models.OrderOffer(order_id=order_id,employee_id=employee_id, price=0)
        )
        
    models.OrderOffer.objects.bulk_create(offer_list)

