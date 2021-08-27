from rest_framework.permissions import AllowAny

from api.views import ListCreateDestroyModelViewSet
from .models import Tag
from .serializers import TagSerializer


class TagView(ListCreateDestroyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [AllowAny, ]
    pagination_class = None
    http_method_names = ['get']
