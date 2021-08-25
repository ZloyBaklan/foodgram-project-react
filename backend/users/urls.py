from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser import views as views_dj

from .views import FollowApiView, FollowListApiView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('djoser.urls')),
    path('users/<int:following_id>/subscribe/', FollowApiView.as_view()),
    path('users/subscriptions/', FollowListApiView.as_view()),
    # path('', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
    path(
        'auth/token/login/',
        views_dj.TokenCreateView.as_view(),
        name='login'
    ),
    path(
        'auth/token/logout/',
        views_dj.TokenDestroyView.as_view(),
        name='login'
    )
]
