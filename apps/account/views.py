from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.account import forms
from apps.account.models import Employee
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView


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


class EmployeeUpdateView(generic.UpdateView):
    template_name = 'account/profile.html'
    success_url = reverse_lazy('panel')
    form_class = forms.EmployeeUserUpdateForm
    
    def get_initial(self):        
        employee = self.get_object()
        self.initial.update({
            'first_name': employee.user.first_name,
            'last_name': employee.user.last_name
        })
        
    def get_object(self):
        employee, created = Employee.objects.get_or_create(user=self.request.user)
        return employee

class CustomerUpdateView(generic.UpdateView):
    template_name = 'account/profile.html'
    success_url = reverse_lazy('panel')
    form_class = forms.CustomerUserUpdateForm
    
    def get_object(self):
        return self.request.user
