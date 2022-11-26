from django.views import generic
from apps.payment.forms import InvoiceCreateForm
from django.urls import reverse_lazy

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404


class InvoiceCreateView(PermissionRequiredMixin, generic.CreateView):
    """ Since there is no actual payment, that's all we need. """
    form_class = InvoiceCreateForm
    template_name = 'new-order.html'
    permission_required = 'order.change_order'
    success_url = reverse_lazy('order-list')