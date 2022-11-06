from django.urls import path
from .views import LoginView, PanelView, RegisterCustomerView, RegisterEmployeeView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/customer/', RegisterCustomerView.as_view(), name='register-customer'),
    path('register/employee/', RegisterEmployeeView.as_view(), name='register-employee'),
    path('panel/', PanelView.as_view(), name='panel'),
]
