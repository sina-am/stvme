from apps.account.models import Employee
from apps.order.models import Order, OrderOffer
from django.db.models import Q, Exists, OuterRef, Count


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


def get_recomendations(user_id: int):
    offer = OrderOffer.objects.filter(employee__user_id=user_id, status=OrderOffer.STALING, order=OuterRef('pk')) 
    return Order.objects.all().annotate(
        recomended=Exists(offer),
        offer_id=offer.values('id')[:1],
        offer_status=offer.values('status')[:1]
    )

def get_customer_orders(user_id: int):
    return Order.objects.filter(customer_id=user_id).annotate(
        offer_count=Count(OrderOffer.objects.filter(order=OuterRef('id'), status=OrderOffer.ACCEPTED).values('id'))
    )