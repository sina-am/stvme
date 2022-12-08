from celery import shared_task
from apps.order import queryset
from apps.order import models


@shared_task
def suggest_to_employee(order_id: int):
    employees = queryset.find_best_match(order_id, None)
    suggest_list = []
    for employee_id in employees.values_list('pk', flat=True):
        suggest_list.append(
            models.Suggest(order_id=order_id,employee_id=employee_id, price=0)
        )
        
    models.Suggest.objects.bulk_create(suggest_list)
