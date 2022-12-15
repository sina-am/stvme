from django.shortcuts import render
from django.views import generic
from apps.order.forms import CreateOrderForm, OrderStatusUpdateForm, CreateOfferForm
from django.urls import reverse_lazy
from apps.order.models import OrderOffer, Order
from apps.order import services
from apps.order import queryset
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect


class ClientOrderCreateView(generic.CreateView):
    form_class = CreateOrderForm
    template_name = 'order/order-create.html'
    success_url = reverse_lazy('order-list')
 
    def form_valid(self, form):
        self.object = form.save(self.request)
        services.offer_to_translator(self.object.pk)
        return HttpResponseRedirect(self.get_success_url())
 

class ClientOrderListView(generic.ListView):
    model = Order
    paginate_by = 5
    template_name = 'order/client-order-list.html'
       
    def get_queryset(self):
        return queryset.get_orders_and_offer().filter(client=self.request.user)


class ClientRecvOfferListView(generic.ListView):
    model = OrderOffer
    paginated_by = 5
    template_name = 'order/client-order-offer-list.html'
   
    def get_queryset(self):
        query = OrderOffer.objects.filter(order__client=self.request.user)
        if self.request.GET.get('order_id'):
            query = query.filter(order_id=int(self.request.GET.get('order_id')))
        return query


class TranslatorOrderListView(generic.ListView):
    model = Order
    paginate_by = 5
    template_name = 'order/translator-order-list.html'
       
    def get_queryset(self):
        return queryset.get_orders_and_offer()

class TranslatorOrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order/translator-order-detail.html'
 

class ClientOrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order/client-order-detail.html'
 

class AcceptedOrderOfferListView(generic.ListView):
    model = OrderOffer
    paginate_by = 10
    template_name = 'order/accepted-offer-list.html'
    
    def check_order_ownership(self, order_id):
        if Order.objects.filter(id=order_id, client=self.request.user).exists():
            return True 
        return False
        
    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        if self.check_order_ownership(order_id):
            return OrderOffer.objects.none()
        
        if order_id:
            return OrderOffer.objects.filter(order_id=order_id, status=OrderOffer.ACCEPTED)
        return OrderOffer.objects.filter(order__client=self.request.user)
     
class FreelancerOrderOfferListView(generic.ListView):
    model = OrderOffer
    paginate_by = 10 
    template_name = 'order/offer-list.html'
    permission_required = 'order.view_offer'
    
    def get_queryset(self):
        return OrderOffer.objects.filter(translator__user=self.request.user).prefetch_related('order')

class OfferCreateView(generic.CreateView):
    form_class = CreateOfferForm
    template_name = 'order/offer-create.html'
    success_url = reverse_lazy('order-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'order': self.get_order()}) 
        return context
    
    def get_order(self):
        if not hasattr(self, 'order'):
            self.order = get_object_or_404(Order, id=self.kwargs['pk'])
        return self.order

    def get(self, request, *args, **kwargs):
        self.order = self.get_order()
        self.object = None
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.object = form.save(self.request.user.translator, self.get_order())
        return HttpResponseRedirect(self.get_success_url())
 

class FreelancerOrderOfferUpdateView(generic.UpdateView):
    model = OrderOffer
    form_class = OrderStatusUpdateForm
    template_name = 'order/offer-detail.html'
    success_url = reverse_lazy('panel')

    def get_queryset(self):
        return OrderOffer.objects.filter(translator__user=self.request.user)