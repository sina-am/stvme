from django.urls import path
from apps.order import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('my/orders/new/', views.ClientOrderCreateView.as_view(), name='new-order'),
    path('my/orders/', views.ClientOrderListView.as_view(), name='client-order-list'),
    path('my/accepted/', views.ClientAcceptedOrderListView.as_view(), name='client-accepted-order-list'),
    path('my/orders/<int:pk>/', views.ClientOrderDetailView.as_view(), name='client-order-detail'),
    path('my/offers/<int:pk>/', views.ClientOfferDetailView.as_view(), name='client-offer-detail'),
    path('my/offers/', views.ClientRecvOfferListView.as_view(), name='client-offer-list'),
    
    path('all/orders/', views.TranslatorOrderListView.as_view(), name='translator-order-list'),
    path('all/orders/<int:pk>', views.TranslatorOrderDetailView.as_view(), name='translator-order-detail'),
    path('all/offers/', views.TranslatorOfferListView.as_view(), name='translator-offer-list'),
]
