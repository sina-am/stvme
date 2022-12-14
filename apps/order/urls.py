from django.urls import path
from apps.order import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('all/orders/', views.AllOrderListView.as_view(), name='all-order-list'),

    path('my/orders/new/', views.OrderCreateView.as_view(), name='new-order'),
    path('my/orders/', views.CustomerOrderListView.as_view(), name='order-list'),
    # path('my/orders/accepted/', views.OrderOfferListView.as_view(), name='accepted-order-list'),
    path('my/orders/<int:pk>/', views.CustomerOrderDetailView.as_view(), name='order-details'),
    
   
    # path('my/jobs/', views.AcceptedOrderOfferListView.as_view(), name='accepted-offer-list'),
    path('my/offers/', views.FreelancerOrderOfferListView.as_view(), name='offer-list'),
    path('my/offers/<int:pk>/', views.FreelancerOrderOfferUpdateView.as_view(), name='offer-details'),
]
