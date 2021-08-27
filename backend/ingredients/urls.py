from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientView

router = DefaultRouter()
router.register('ingredients', IngredientView, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
