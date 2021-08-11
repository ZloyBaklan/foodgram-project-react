from rest_framework import filters, viewsets, status
from rest_framework.views import APIView
from .serializers import RecipeSerializer
from .models import Recipe, Favorite
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from .permissions import IsOwnerOrReadOnly

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
    http_method_names = ['get', 'post', 'put', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, pk=None):
        data_in = request.data
        print(data_in)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)

        if instance is None:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            lookup_value = self.kwargs[lookup_url_kwarg]
            extra_kwargs = {self.lookup_field: lookup_value}
            serializer.save(**extra_kwargs)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer.save()
        data_out = serializer.data
        return Response(serializer.data)
    
@action(detail=True, methods=['get', 'delete'], url_path='favorite', permission_classes = IsOwnerOrReadOnly)
def favorite(self, request, pk=None):
    if request.method == 'GET':
        Favorite.objects.get_or_create(user=request.user)
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        Favorite.objects.filter(user=request.user).delete()
        return Response(status)
    
''' 
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        # filter by a variable captured from url, for example
        return qs
    
    def post(self, request, *args, **kwargs):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            ingredient = serializer.save()
            serializer = RecipeSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''