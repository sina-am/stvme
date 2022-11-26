from django.db import models


class Invoice(models.Model):
    STATUS = (
        ('PRE_INVOICE', 'Pre-invoice'),
        ('INVOICE', 'Invoice')
    )
    suggest = models.ForeignKey('order.Suggest', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=12, default='PRE_INVOICE')