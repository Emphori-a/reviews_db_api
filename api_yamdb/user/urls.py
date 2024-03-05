from django.urls import path

from .views import SignupView, TokenView, UserProfile

urlpatterns = [
    path('v1/users/', UserProfile.as_view(), name='profile'),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view, name='get_token'),
]
