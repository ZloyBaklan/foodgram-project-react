import datetime
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Favorite, IngredientAmount, Recipe, ShoppingList
from .permissions import IsOwnerOrReadOnly
from .serializers import (FavoriteSerializer, RecipeFullSerializer,
                          RecipeSerializer, ShoppingListSerializer)


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
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6
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
    # queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, favorite_id):
        user = request.user
        data = {
            'favorite': favorite_id,
            'user': user.id
        }
        serializer = FavoriteSerializer(data=data,
                                        context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, favorite_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=favorite_id)
        favorite = get_object_or_404(Favorite, user=user, favorite=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, recipe_id):
        user = request.user
        data = {
            'recipe': recipe_id,
            'user': user.id
        }
        serializer = ShoppingListSerializer(data=data,
                                            context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        in_list = get_object_or_404(ShoppingList, user=user, recipe=recipe)
        in_list.delete()
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
        today = datetime.date.today()
        main_list.append(f'\n From FoodGram with love, {today.year}')
        response = HttpResponse(main_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="BuyList.txt"'
        return response
