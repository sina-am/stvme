from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy

from .forms import AuthForm, RegisterCustomerForm, RegisterEmployeeForm
from django.contrib.auth import login


class PanelView(generic.TemplateView):
    template_name = 'panel.html'

class LoginView(generic.FormView):
    template_name = 'login.html'
    success_url = reverse_lazy('panel')
    form_class = AuthForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
        

class RegisterCustomerView(generic.CreateView):
    form_class = RegisterCustomerForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class RegisterEmployeeView(generic.CreateView):
    form_class = RegisterEmployeeForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
