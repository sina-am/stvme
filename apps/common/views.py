from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from apps.account.models import Translator
from apps.order.models import OrderOffer
from django.db.models import OuterRef, Subquery, Count


class PanelView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panel/panel.html'
        
        
class IndexView(generic.TemplateView):
    template_name = 'panel/index.html' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"top_translators": self.get_queryset()})
        return context
        
    def get_queryset(self):
        accepted_offers = OrderOffer.objects.filter(status=OrderOffer.ACCEPTED).values('translator').annotate(total=Count('pk')).order_by('total')
        return accepted_offers