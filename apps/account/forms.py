from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from apps.account.models import User, Translator


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'role')

    role = forms.ChoiceField(choices=User.ROLES, label="register as")
    template_name = 'components/form.html'
    
    def save(self):
        return User.objects.create_user(
            email=self.instance.email,
            first_name=self.instance.first_name,
            last_name=self.instance.last_name,
            password=self.cleaned_data["password1"],
            role=self.instance.role
        )


class AuthForm(AuthenticationForm):
    template_name = 'components/form.html'


class CustomerUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
    template_name = 'components/form.html'


class TranslatorUserUpdateForm(forms.ModelForm):
    class Meta:
        model = Translator
        exclude = ('user', 'credit')
        
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    template_name = 'components/form.html'
   
    def save(self):
        self.instance.user.first_name = self.cleaned_data["first_name"]
        self.instance.user.last_name = self.cleaned_data["last_name"]
        self.instance.user.save()
        return super().save()

