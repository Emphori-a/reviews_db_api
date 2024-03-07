from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignupView, TokenView, UserProfile

v1_router = DefaultRouter()
v1_router.register('users', UserProfile)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='get_token'),
]
