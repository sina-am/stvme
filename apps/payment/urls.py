from django.urls import path
from apps.payment import views


urlpatterns = [
    path('', views.InvoiceCreateView.as_view(), name='payment')
]