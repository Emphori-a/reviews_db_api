from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, SignupView, TitleViewSet,
                    TokenView, UserProfileSet)


router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('users', UserProfileSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', TokenView.as_view(), name='get_token'),
]
