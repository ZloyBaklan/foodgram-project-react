from ingredients.models import Ingredient
from rest_framework import filters, viewsets, status
from rest_framework.views import APIView
from .serializers import RecipeFullSerializer, RecipeSerializer, FavoriteSerializer, ShoppingListSerializer
from .models import IngredientAmount, Recipe, Favorite, ShoppingList
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, HttpResponse
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (IsAuthenticatedOrReadOnly, IsAuthenticated)
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView


class ListCreateDestroyModelViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    A viewset that provides default `list()`, `create()`, 'destroy()' actions.
    """
    pass

class RecipeViewSet(ListCreateDestroyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    #pagination_class = pagination.PageNumberPagination
    #pagination_class.page_size = 6
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', ]
    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeFullSerializer
        return RecipeSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
class FavoriteApiView(APIView):
    #queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request, favorite_id):
        user = request.user
        data = {
            'favorite': favorite_id,
            'user': user.id
        }
        serializer = FavoriteSerializer(data=data, context={'request':request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, favorite_id):
        user = request.user
        favorite = get_object_or_404(Recipe, id=favorite_id)
        Favorite.objects.get(user=user, favorite=favorite).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, recipe_id):
        user = request.user
        data = {
            'recipe': recipe_id,
            'user': user.id
        }
        serializer = ShoppingListSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingList.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DownloadShoppingCart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shopping_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__purchases__user=request.user
        )
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                shopping_list[name]['amount'] += amount
        main_list = ([f"{item}/{value['amount']}/{value['measurement_unit']}"
                     for item, value in shopping_list.items()])
        today = date.today()
        main_list.append(f'\n From FoodGram with love, {today.year}')
        response = HttpResponse(main_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="BuyingList.txt"'
        return response