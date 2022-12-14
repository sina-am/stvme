from django.urls import path
from apps.common.views import PanelView, IndexView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', PanelView.as_view(), name='panel'),
]