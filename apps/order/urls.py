from django.urls import path
from apps.order import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('orders/new/', views.OrderCreateView.as_view(), name='new-order'),
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-details'),
    path('suggests/', views.SuggestListView.as_view(), name='suggest-list'),
    path('suggests/<int:pk>/', views.SuggestUpdateView.as_view(), name='suggest-details'),
]
