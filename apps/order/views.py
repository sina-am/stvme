from django.shortcuts import render
from django.views import generic
from apps.order.forms import CreateOrderForm, OrderStatusUpdateForm
from django.urls import reverse_lazy
from apps.order.models import OrderOffer, Order
from apps.order import services
from apps.order import queryset
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect


class OrderCreateView(generic.CreateView):
    form_class = CreateOrderForm
    template_name = 'order/order-create.html'
    success_url = reverse_lazy('order-list')
 
    def form_valid(self, form):
        self.object = form.save(self.request)
        services.offer_to_employee(self.object.pk)
        return HttpResponseRedirect(self.get_success_url())


class AllOrderListView(generic.ListView):
    model = Order
    paginate_by = 5
    template_name = 'order/order-all-list.html'
    
    def get_queryset(self):
        return queryset.get_recomendations(self.request.user.pk)
             

class CustomerOrderListView(generic.ListView):
    model = Order
    paginate_by = 5
    template_name = 'order/order-list.html'
    
    def get_queryset(self):
        return queryset.get_customer_orders(self.request.user.id) 
    

class CustomerOrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order/order-detail.html'
    
    def get_context_data(self, **kwargs):
        kwargs.update({})
        return super().get_context_data(**kwargs)
        
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    

class AcceptedOrderOfferListView(generic.ListView):
    model = OrderOffer
    paginate_by = 10
    template_name = 'order/accepted-offer-list.html'
    
    def check_order_ownership(self, order_id):
        if Order.objects.filter(id=order_id, customer=self.request.user).exists():
            return True 
        return False
        
    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        if self.check_order_ownership(order_id):
            return OrderOffer.objects.none()
        
        if order_id:
            return OrderOffer.objects.filter(order_id=order_id, status=OrderOffer.ACCEPTED)
        return OrderOffer.objects.filter(order__customer=self.request.user)
     
class FreelancerOrderOfferListView(generic.ListView):
    model = OrderOffer
    paginate_by = 10 
    template_name = 'order/offer-list.html'
    permission_required = 'order.view_offer'
    
    def get_queryset(self):
        return OrderOffer.objects.filter(employee__user=self.request.user).prefetch_related('order')


class FreelancerOrderOfferUpdateView(generic.UpdateView):
    model = OrderOffer
    form_class = OrderStatusUpdateForm
    template_name = 'order/offer-detail.html'
    success_url = reverse_lazy('panel')

    def get_queryset(self):
        return OrderOffer.objects.filter(employee__user=self.request.user)