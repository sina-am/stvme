from django.shortcuts import render
from django.views import generic
from apps.order.forms import CreateOrderForm, OrderStatusUpdateForm, CreateOfferForm, UpdateOfferStatusForm
from django.urls import reverse_lazy
from apps.order.models import OrderOffer, Order, AcceptedOrder
from apps.account.models import Translator  
from apps.order import services
from apps.order import queryset
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect
from django.db.models import OuterRef, Exists
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from apps.payment.models import Bank


class ClientOrderCreateView(generic.CreateView):
    form_class = CreateOrderForm
    template_name = 'order/order-create.html'
    success_url = reverse_lazy('client-order-list')
 
    def form_valid(self, form):
        self.object = form.save(self.request)
        # services.offer_to_translator(self.object.pk)
        messages.success(self.request, _("order successfuly created"))
        return HttpResponseRedirect(self.get_success_url())
 

class ClientOrderListView(generic.ListView):
    model = Order
    paginate_by = 5
    template_name = 'client/order-list.html'
       
    def get_queryset(self):
        return queryset.get_orders_and_offer().filter(client=self.request.user)


class ClientAcceptedOrderListView(generic.ListView):
    model = AcceptedOrder
    paginate_by = 5
    template_name = 'client/accepted-order-list.html'
       
    def get_queryset(self):
        return AcceptedOrder.objects.filter(order__client=self.request.user)



class ClientOrderDetailView(generic.TemplateView):
    template_name = 'client/order-detail.html'
    form_class = UpdateOfferStatusForm
     
    def get_order(self):
        return get_object_or_404(Order, id=self.kwargs.get('pk'))
   
    def get_offers(self):
        return OrderOffer.objects.filter(
            order=self.get_order()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.get_order()
        context["offer_list"] = self.get_offers()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            offer = get_object_or_404(OrderOffer, id=form.cleaned_data["offer_id"])
            return self.update_offer(offer, form.cleaned_data["status"])
        else:
            return self.invalid_form(form)
     
    def update_offer(self, offer, status):
        if status == OrderOffer.REJECTED:
            offer.status = status
            offer.save()
        return self.render_to_response(self.get_context_data())   


class ClientOfferDetailView(generic.DetailView):
    model = OrderOffer 
    template_name = 'client/offer-detail.html'

    def get_queryset(self):
        return OrderOffer.objects.filter(order__client=self.request.user)
    
    def get_banks(self):
        return Bank.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["banks"] = self.get_banks()
        return context
    
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
    template_name = 'translator/order-list.html'
       
    def get_queryset(self):
        return queryset.get_orders_and_offer()


class TranslatorOfferListView(generic.ListView):
    template_name = 'translator/offer-list.html'
    form_class = CreateOfferForm
    model = OrderOffer
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.valid_form(form)
        else:
            self.invalid_form(form)
            
    def valid_form(self, form):
        offer = form.save(Translator.objects.get(user=self.request.user))
        return self.render_to_response(self.get_context_data())

    def invalid_form(self, form):
        return self.render_to_response(self.get_context_data())

    def get_my_offer(self):
        """ Check whether the current user had an offer on the order """
        try:
            return self.get_queryset().get(translator__user_id=self.request.user.id)       
        except OrderOffer.DoesNotExist:
            return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_id"] = self.request.GET.get('order_id') 
        context["my_offer"] = self.get_my_offer()
        return context
    
    def get_queryset(self):
        query = OrderOffer.objects.filter(status=OrderOffer.STALING)
        
        order_id = self.request.GET.get('order_id')
        if order_id:
            return query.filter(order_id=order_id)
        return query
    

class TranslatorOrderDetailView(generic.DetailView):
    template_name = 'translator/order-detail.html'
    model = Order 

    def get_queryset(self):
        return Order.objects.all()
    