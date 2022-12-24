from django.urls import path
from apps.payment import views


urlpatterns = [
    path('invoices/new', views.InvoiceCreateView.as_view(), name='new-invoice'),
]