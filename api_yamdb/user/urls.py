from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignupView, TokenView


urlpatterns = [
    path('v1/users', SignupView),
    path('v1/auth/signup/', SignupView, name='signup'),
    path('v1/auth/token/', TokenView, name='get_token'),
]
