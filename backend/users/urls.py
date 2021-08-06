from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import UserFollowViewSet

router = DefaultRouter()
router.register(r'users/(?P<user_id>\d+)/subscribe', UserFollowViewSet)
urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
