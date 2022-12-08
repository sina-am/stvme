from apps.account.models import Employee
from apps.order.models import Order
from django.db.models import Q


def find_best_match(order_id: int, price: int):
    """Find the best editors or translators for the given order
    Criterias include: language match, availablity of the employee and field match
    """
    
    order = Order.objects.get(id=order_id)
    return Employee.objects.filter(
        languages=order.source_language,
        is_available=True,
        specialized_fields=order.specialized_field
    ).filter(languages=order.target_language).order_by('-max_time', 'min_charge')[:3]