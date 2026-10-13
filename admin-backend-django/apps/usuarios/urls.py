from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, usuario_actual

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('yo/', usuario_actual, name='usuario-actual'),
]
