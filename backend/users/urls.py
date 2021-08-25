from django.urls import include, path, re_path

from .views import FollowApiView, FollowListApiView

urlpatterns = [
    # path('auth/', include('djoser.urls')),
    path('users/<int:following_id>/subscribe/', FollowApiView.as_view()),
    path('users/subscriptions/', FollowListApiView.as_view()),
    path('', include('djoser.urls')),
    re_path(r'^users/auth/', include('djoser.urls.authtoken')),
]
