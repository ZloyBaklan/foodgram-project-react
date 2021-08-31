from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from .models import Tag
from .serializers import TagSerializer


class TagView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [AllowAny, ]
    pagination_class = None
