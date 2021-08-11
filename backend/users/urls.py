from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import FollowApiView, FollowListApiView
from rest_framework.urlpatterns import format_suffix_patterns
router = DefaultRouter()
#router.register(r'^subscribe', UnfollowFollowViewSet)
#router.register(r'^subscriptions', UserFollowViewSet)
urlpatterns = [
    path('users/<int:following_id>/subscribe/', FollowApiView.as_view()),
    path('users/subscriptions/', FollowListApiView.as_view()),
    path('', include('djoser.urls')),
    #path('users/', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
