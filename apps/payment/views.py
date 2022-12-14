from django.views import generic
from apps.payment.forms import InvoiceCreateForm
from django.urls import reverse_lazy

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http.response import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404


class InvoiceCreateView(generic.FormView):
    """ Since there is no actual payment, that's all we need. """

    form_class = InvoiceCreateForm
    success_url = reverse_lazy('order-list')

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            print(form.errors)
            return HttpResponseBadRequest(form.errors)