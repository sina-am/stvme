from django.urls import path
from apps.account import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('profile/employee/', views.EmployeeUpdateView.as_view(), name='profile-employee'),
    path('profile/customer/', views.CustomerUpdateView.as_view(), name='profile-customer'),
]
