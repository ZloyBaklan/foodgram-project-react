from django.urls import include, path

from djoser import views as views_dj

from .views import FollowApiView, FollowListApiView

urlpatterns = [
    # path('auth/', include('djoser.urls')),
    path('users/<int:following_id>/subscribe/', FollowApiView.as_view()),
    path('users/subscriptions/', FollowListApiView.as_view()),
    path('', include('djoser.urls')),
    path(
        'api/auth/token/login/',
        views_dj.TokenCreateView.as_view(),
        name='login'
    ),
    path(
        'api/auth/token/logout/',
        views_dj.TokenDestroyView.as_view(),
        name='login'
    )
]
