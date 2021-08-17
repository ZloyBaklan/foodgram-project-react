from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.response import Response

from api.views import ListCreateDestroyModelViewSet
from .models import Tag
from .serializers import TagSerializer


class TagView(ListCreateDestroyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', ]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        # original qs
        qs = super().get_queryset()
        # filter by a variable captured from url, for example
        return qs

    def post(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            ingredient = serializer.save()
            serializer = TagSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
