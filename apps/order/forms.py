from django import forms
from apps.order.models import Order, Suggest
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
    
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Register', css_class='btn-primary'))

    def save(self, request):
        self.instance.customer = request.user
        return super().save()


class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Suggest
        fields = (
            'status', 
        )
    
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Register', css_class='btn-primary'))
    status = forms.ChoiceField(
        choices=(
            (Suggest.ACCEPTED, "accept"), 
            (Suggest.REJECTED, 'rejected')
        )
    )
