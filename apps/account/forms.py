from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from apps.account.models import User, Employee


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'role')

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Register', css_class='btn-primary'))

    def save(self):
        return User.objects.create_user(
            email=self.instance.email,
            first_name=self.instance.first_name,
            last_name=self.instance.last_name,
            password=self.cleaned_data["password1"],
            role=self.instance.role
        )


class AuthForm(AuthenticationForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Login', css_class='btn-primary'))


class CustomerUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Change', css_class='btn-primary'))


class EmployeeUserUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ('user', )
        
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Change', css_class='btn-primary'))
    
    def save(self):
        self.instance.user.first_name = self.cleaned_data["first_name"]
        self.instance.user.last_name = self.cleaned_data["last_name"]
        self.instance.user.save()
        return super().save()

