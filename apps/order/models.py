from django.db import models
from apps.account.models import SpecializedField

class Order(models.Model):
    STATUS = (
        ('INVALID_ORDER', 'invalid order'),
        ('ESTIMATING_PRICE', 'waiting for estimation'),
        ('WAITING', 'waiting for accept')
    )
    TYPES = (
        ('EDIT', 'Edit'),
        ('TRANSLATION', 'Translation'),
        ('BOTH', 'Both')
    )

    text = models.TextField()
    deadline = models.DateTimeField()
    specialized_field = models.ManyToManyField(SpecializedField)
    status = models.CharField(choices=STATUS, max_length=20)
    type = models.CharField(choices=TYPES, max_length=12)