from django.contrib import admin
from apps.payment.models import Bank, Invoice
# Register your models here.
admin.site.register(Bank)
admin.site.register(Invoice)

