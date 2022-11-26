from django.urls import path
from apps.panel.views import PanelView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', PanelView.as_view(), name='panel')
]