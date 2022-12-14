from django import forms
from apps.order.models import Order, OrderOffer
from apps.order import services
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'description', 'original_text',
            'deadline', 'specialized_field', 
            'type', 'source_language', 'target_language'
        )
         
    template_name = 'components/form.html'
    
    def save(self, request):
        self.instance.customer = request.user
        return super().save()


class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderOffer
        fields = (
            'status', 
        ) 

    status = forms.ChoiceField(
        choices=(
            (OrderOffer.ACCEPTED, "accept"), 
            (OrderOffer.REJECTED, 'rejected')
        ),
        label='Request'
    )
