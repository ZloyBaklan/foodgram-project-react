from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DownloadShoppingCart, RecipeViewSet, FavoriteApiView, ShoppingView

router = DefaultRouter()
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('recipes/<int:favorite_id>/favorite/', FavoriteApiView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart', ShoppingView.as_view()),
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('', include(router.urls)),
]