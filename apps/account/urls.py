from django.urls import path
from apps.account import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('profile/translator/', views.TranslatorUpdateView.as_view(), name='translator-update'),
    path('profile/client/', views.ClientUpdateView.as_view(), name='client-update'),

    path('translators/', views.TranslatorListView.as_view(), name='translator-list'),
    path('translators/<int:pk>', views.TranslatorDetailView.as_view(), name='translator-detail')
]
