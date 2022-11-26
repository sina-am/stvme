from django.shortcuts import render
from django.views import generic
from apps.order.forms import CreateOrderForm, OrderStatusUpdateForm
from django.urls import reverse_lazy
from apps.order.models import Suggest, Order
from apps.order import services
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404


class OrderCreateView(PermissionRequiredMixin, generic.CreateView):
    form_class = CreateOrderForm
    template_name = 'new-order.html'
    permission_required = 'order.view_order'
    success_url = reverse_lazy('order-list')

    def form_valid(self, form):
        self.object = form.save(self.request)
        # TODO: Create suggestions with Celery tasks.
        # services.suggest_to_employee(self.object)
        return super().form_valid(form)


class OrderListView(PermissionRequiredMixin, generic.ListView):
    model = Order
    paginate_by = 10 
    template_name = 'order-list.html'
    permission_required = 'order.view_order'
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    

class OrderDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'order-details.html'
    permission_required = 'order.view_order'
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    
    
class SuggestListView(PermissionRequiredMixin, generic.ListView):
    model = Suggest
    paginate_by = 10 
    template_name = 'suggest-list.html'
    permission_required = 'order.view_suggest'
    
    def get_queryset(self):
        return Suggest.objects.filter(employee=self.request.user).prefetch_related('order')


class SuggestUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Suggest
    form_class = OrderStatusUpdateForm
    template_name = 'suggest-details.html'
    permission_required = 'order.view_suggest'
    success_url = reverse_lazy('panel')

    def get_queryset(self):
        return Suggest.objects.filter(employee=self.request.user)