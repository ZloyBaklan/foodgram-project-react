from django.urls import include, path

from .views import FollowApiView, FollowListApiView

urlpatterns = [
    path('users/<int:following_id>/subscribe/', FollowApiView.as_view()),
    path('users/subscriptions/', FollowListApiView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
