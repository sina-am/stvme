from django.db import models
from apps.payment.models import Invoice
from apps.common.models import Language, SpecializedField
from django.utils.translation import gettext_lazy as _
from _md5 import md5
import pathlib


def upload_order_filename(instance, filename):
    file_extension = pathlib.Path(filename).suffix
    file_hash = md5(filename.encode('utf-8')).hexdigest()
    return 'documents/orders/{0}/{1}'.format(
        instance.client.id, file_hash + file_extension)


class Order(models.Model):
    """Create by client for either translation text or editing text order
    This will then display to freelancers for them to offer a OrderOffer
    """
    WAITING_FOR_PAYMENT = 'WAITING_FOR_PAYMENT'
    WAITING_FOR_ACCEPT = 'WAITING_FOR_ACCEPT'
    IN_PROGRESS = 'IN_PROGRESS'
    STATUS = (
        ('INVALID_ORDER', 'invalid order'),
        (WAITING_FOR_PAYMENT, 'waiting for payment'),
        (WAITING_FOR_ACCEPT, 'waiting for accept')
    )
    
    client = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='client')
    description = models.TextField(null=True, blank=True)
     
    text = models.FileField(upload_to=upload_order_filename)
    text_length = models.IntegerField()
    deadline = models.DateTimeField()
    specialized_field = models.ForeignKey(SpecializedField, on_delete=models.CASCADE, null=True, blank=True)
    source_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='source_language')
    target_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='target_language')
    edit_needed = models.BooleanField(default=True) 

    def save(self):
        self.text_length = 100 
        return super().save()
        
    def get_text_length(self):
        return 500 
    
    def estimated_price(self):
        return self.get_text_length() * 20
    
    @property
    def status(self):
        queryset = OrderOffer.objects.filter(status=OrderOffer.ACCEPTED, order=self)
        if queryset.exists():
            if Invoice.objects.filter(offer__in=queryset).exists():
                return self.IN_PROGRESS
            return self.WAITING_FOR_PAYMENT
        return self.WAITING_FOR_ACCEPT
   
    def accept_offer(self):
        return self.status == self.WAITING_FOR_ACCEPT
     
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(source_language=models.F('target_language')),
                name=_("source and target language can't be the same"),
            )
        ]


class OrderOffer(models.Model):
    """ Create by freelancer for a order
    """
    REJECTED = 'REJECTED'
    ACCEPTED = 'ACCEPTED'
    STALING = 'STALING'
    TYPES = (
        (REJECTED, 'Rejected'),
        (ACCEPTED, 'Accepted'),
        (STALING, 'Staling')
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    translator = models.ForeignKey('account.Translator', on_delete=models.CASCADE)
    status = models.CharField(choices=TYPES, max_length=12, default='STALING')
    price = models.DecimalField(max_digits=5, decimal_places=2)
      
    
class AcceptedOrderOffer(models.Model):
    offer = models.OneToOneField(OrderOffer, on_delete=models.CASCADE) 
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
