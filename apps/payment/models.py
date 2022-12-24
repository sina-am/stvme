from django.db import models, transaction
from apps.order.models import Order, OrderOffer, AcceptedOrder


class Bank(models.Model):
    name = models.CharField(max_length=100)
    icon = models.FileField()
    
    
class Invoice(models.Model):
    offer = models.OneToOneField('order.OrderOffer', on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):        
        with transaction.atomic():
            super().save()
            self.offer.status = OrderOffer.ACCEPTED 
            self.offer.save()
            self.offer.order.status = Order.IN_PROGRESS
            self.offer.order.save()

            AcceptedOrder.objects.create(order=self.offer.order, offer=self.offer)