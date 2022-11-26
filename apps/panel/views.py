from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class PanelView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panel/panel.html'
        
        