from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response

from api.views import ListCreateDestroyModelViewSet
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientView(ListCreateDestroyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', ]
    http_method_names = ['get', 'post']

    def post(self, request, *args, **kwargs):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            ingredient = serializer.save()
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
