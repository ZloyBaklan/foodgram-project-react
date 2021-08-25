from django.urls import include, path, re_path
from rest_framework.authtoken import views

from .views import FollowApiView, FollowListApiView

# router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    # path('', include(router.urls)),
    path('', include('djoser.urls')),
    #path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:following_id>/subscribe/', FollowApiView.as_view()),
    path('users/subscriptions/', FollowListApiView.as_view()),
    # path('', include('djoser.urls')),
    re_path(r'^auth/', include(views.obtain_auth_token)),
    # path(
    #    'auth/token/login/',
    #    views_dj.TokenCreateView.as_view(),
    #    name='login'
    # ),
    # path(
    #    'auth/token/logout/',
    #    views_dj.TokenDestroyView.as_view(),
    #    name='login'
    # )
]
