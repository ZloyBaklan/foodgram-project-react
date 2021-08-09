from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagView

router = DefaultRouter()
router.register('tags', TagView)

urlpatterns = [
    path('', include(router.urls)),
]