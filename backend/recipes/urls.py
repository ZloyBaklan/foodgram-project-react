from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingCart, FavoriteApiView, RecipeViewSet,
                    ShoppingView, IngredientView)

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register(r'ingredients', IngredientView, basename='ingredients')

urlpatterns = [
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('', include(router.urls)),
    path('recipes/<int:favorite_id>/favorite/', FavoriteApiView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingView.as_view()),
]
