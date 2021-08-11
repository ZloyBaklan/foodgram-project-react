from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework.response import Response
from django.db.models.fields.related import ForeignKey
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework import filters, serializers, status
from .models import CustomUser, Follow
from .serializers import UserFollowSerializer, FollowListSerializer
from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework.views import APIView


class FollowApiView(APIView):
    #queryset = Follow.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, following_id):
        user = request.user
        data = {
            'following': following_id,
            'user': user.id
        }
        serializer = UserFollowSerializer(data=data, context={'request':request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def delete(self, request, following_id):
        user = request.user
        following = get_object_or_404(CustomUser, id=following_id)
        Follow.objects.filter(user=user, following=following).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FollowListApiView(APIView):
    permission_classes = [IsAuthenticated] 
    #queryset = Follow.objects.all() 
    serializer_class = FollowListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(following__user=user)
