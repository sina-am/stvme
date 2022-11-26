from apps.order import queryset
from apps.order import models
from apps.payment.models import Invoice
from django.db import transaction
import datetime


def suggest_to_employee(order):
    return None
