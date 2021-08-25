from django_filters.rest_framework import DjangoFilterBackend

from api.views import ListCreateDestroyModelViewSet
from .models import Tag
from .serializers import TagSerializer


class TagView(ListCreateDestroyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', ]
    http_method_names = ['get', 'post']
