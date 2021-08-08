from rest_framework import filters, viewsets, status
from rest_framework.views import APIView
from .serializers import RecipeSerializer
from .models import Recipe
from rest_framework.response import Response

class ListCreateDestroyModelViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    A viewset that provides default `list()`, `create()`, 'destroy()' actions.
    """
    pass

class RecipeViewSet(ListCreateDestroyModelViewSet):
    serializer_class = RecipeSerializer
    #permission_classes = [IsAdminOrReadOnly]
    queryset = Recipe.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'id'