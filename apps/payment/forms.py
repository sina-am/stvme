from django import forms
from apps.payment.models import Invoice


class InvoiceCreateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('offer', )
       