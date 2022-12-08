from django.db import models
from apps.account.models import SpecializedField
from apps.payment.models import Invoice
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    WAITING_FOR_PAYMENT = 'WAITING_FOR_PAYMENT'
    WAITING_FOR_ACCEPT = 'WAITING_FOR_ACCEPT'
    IN_PROGRESS = 'IN_PROGRESS'
    STATUS = (
        ('INVALID_ORDER', 'invalid order'),
        (WAITING_FOR_PAYMENT, 'waiting for payment'),
        (WAITING_FOR_ACCEPT, 'waiting for accept')
    )
    TYPES = (
        ('EDIT', 'Edit'),
        ('TRANSLATION', 'Translation'),
        ('BOTH', 'Both')
    )

    customer = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='customer')
    description = models.CharField(max_length=600, null=True, blank=True)
    # TODO: Probebly should be separated models
    original_text = models.TextField()
    translated_text = models.TextField(null=True, blank=True)
    edited_text = models.TextField(null=True, blank=True)

    deadline = models.DateTimeField()
    specialized_field = models.ForeignKey(SpecializedField, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(choices=TYPES, max_length=12)
    source_language = models.ForeignKey('account.Language', on_delete=models.CASCADE, related_name='source_language')
    target_language = models.ForeignKey('account.Language', on_delete=models.CASCADE, related_name='target_language')

    def get_text_length(self):
        return len(self.original_text)
    
    def calculate_price(self):
        return self.get_text_length() * 20
    
    @property
    def status(self):
        queryset = Suggest.objects.filter(status=Suggest.ACCEPTED, order=self)
        if queryset.exists():
            if Invoice.objects.filter(suggest__in=queryset).exists():
                return self.IN_PROGRESS
            return self.WAITING_FOR_PAYMENT
        return self.WAITING_FOR_ACCEPT
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(source_language=models.F('target_language')),
                name=_("source and target language can't be the same"),
            )
        ]


class Assign(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    employee = models.ForeignKey('account.User', on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()


class Suggest(models.Model):
    REJECTED = 'REJECTED'
    ACCEPTED = 'ACCEPTED'
    STALING = 'STALING'
    TYPES = (
        (REJECTED, 'Rejected'),
        (ACCEPTED, 'Accepted'),
        (STALING, 'Staling')
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    employee = models.ForeignKey('account.User', on_delete=models.CASCADE)
    status = models.CharField(choices=TYPES, max_length=12, default='STALING')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    
    def accept_order(self):
        self.status = self.ACCEPTED
        self.order.status = WAITING_FOR_PAYMENT
