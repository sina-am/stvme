from django import forms
from apps.order.models import Order, OrderOffer
from apps.order import services
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'text', 'specialized_field',
            'source_language', 'target_language',
            'description', 'deadline', 'edit_needed'
        )
         
    template_name = 'components/form.html'
    
    def save(self, request):
        self.instance.client = request.user
        return super().save()

class CreateOfferForm(forms.ModelForm):
    class Meta:
        model = OrderOffer
        fields = (
            'order',
            'price',
        )
         
    template_name = 'components/form.html'
    
    def save(self, translator):
        self.instance.translator = translator
        return super().save()

class UpdateOfferStatusForm(forms.Form):
    status = forms.ChoiceField(choices=OrderOffer.TYPES)
    offer_id = forms.IntegerField() 
    template_name = 'components/form.html'


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
