from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.account import forms
from apps.account.models import Translator
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class LoginView(generic.FormView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('panel')
    form_class = forms.AuthForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
    
    
class LogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('login')
       

class UserRegisterView(generic.CreateView):
    form_class = forms.UserRegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('login')



class ProfileUpdateView(generic.UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_url"] = self.action_url 
        return context

    def form_valid(self, form):
        messages.success(self.request, _("profile updated successfully"))
        return super().form_valid(form)
     
 
class TranslatorUpdateView(ProfileUpdateView):
    template_name = 'account/profile.html'
    success_url = reverse_lazy('panel')
    form_class = forms.TranslatorUserUpdateForm
    action_url = 'translator-update'

    def get_initial(self):        
        translator = self.get_object()
        self.initial.update({
            'first_name': translator.user.first_name,
            'last_name': translator.user.last_name
        })
        
    def get_object(self):
        translator, created = Translator.objects.get_or_create(user=self.request.user)
        return translator

class ClientUpdateView(ProfileUpdateView):
    template_name = 'account/profile.html'
    success_url = reverse_lazy('panel')
    form_class = forms.CustomerUserUpdateForm
    action_url = 'client-update'
   
    def get_object(self):
        return self.request.user


class TranslatorListView(generic.ListView):
    template_name = 'account/user-list.html'
    paginate_by = 5
    
    def get_queryset(self):
        return Translator.objects.all().order_by('user__email')

class TranslatorDetailView(generic.DetailView):
    template_name = 'account/user-detail.html'
    model = Translator 