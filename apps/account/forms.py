from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from apps.account.models import Employee


class RegisterCustomerForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Register', css_class='btn-primary'))


class RegisterEmployeeForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = (
            'email', 'password1', 'password2', 
            'languages', 'specialized_field', 'min_charge',
            'max_charge', 'max_time', 'min_time')

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Register', css_class='btn-primary'))

    email = forms.EmailField(max_length=100)


class AuthForm(AuthenticationForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Login', css_class='btn-primary'))
