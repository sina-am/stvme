from apps.account.models import Translator
from apps.order.models import Order, OrderOffer
from django.db.models import Q, Exists, OuterRef, Count


def find_best_match(order_id: int, price: int):
    """Find the best editors or translators for the given order
    Criterias include: language match, availablity of the translator and field match
    """
    
    order = Order.objects.get(id=order_id)
    return Translator.objects.filter(
        languages=order.source_language,
        is_available=True,
        specialized_fields=order.specialized_field
    ).filter(languages=order.target_language).order_by('-max_time', 'min_charge')[:3]


def get_recomendations(user_id: int):
    offer = OrderOffer.objects.filter(translator__user_id=user_id, status=OrderOffer.STALING, order=OuterRef('pk')) 
    return Order.objects.all().annotate(
        recomended=Exists(offer),
        offer_id=offer.values('id')[:1],
        offer_status=offer.values('status')[:1]
    )

def get_orders_and_offer():
    return Order.objects.all().annotate(
        offer_count=Count(OrderOffer.objects.filter(order=OuterRef('id')).values('id'))
    )
