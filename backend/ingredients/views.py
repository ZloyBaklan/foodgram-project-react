from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.views import ListCreateDestroyModelViewSet
from .filters import IngredientFilter
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientView(ListCreateDestroyModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]
    queryset = Ingredient.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filter_class = IngredientFilter
    pagination_class = None
    http_method_names = ['get']
