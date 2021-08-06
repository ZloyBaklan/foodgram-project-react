from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.fields.related import ForeignKey
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import filters, status
from .models import Follow, CustomUser
from .serializers import UserFollowSerializer
from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets

class UserFollowViewSet(viewsets.ModelViewSet): 
    permission_classes = [IsAuthenticated] 
    queryset = Follow.objects.all() 
    serializer_class = UserFollowSerializer 
    filter_backends = [filters.SearchFilter] 
    search_fields = ['user__username', 'author__username'] 
    http_method_names = ['get', 'post', 'delete'] 
 
    def get_queryset(self): 
        user = get_object_or_404(CustomUser, username=self.request.user.username) 
        return user.following
 
    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)

'''
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, status
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from djoser.conf import django_settings
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny,IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import CustomUser
from .serializers import UserSerializer
from .permissions import IsOwnerProfile, Allow

from djoser.views import UserViewSet

class FoodgramUserViewSet(UserViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = Allow
    lookup_field = 'id'
    # filterset_fields = ['id']
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['id']
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        id = self.request.user.pk
        #user = self.request.user
        queryset = CustomUser.objects.all()
        #if  self.action == "list":
            #queryset = queryset.filter(pk=id)
        return queryset

    @action(["get"], permission_classes=[Allow], detail=False)
    def get_queryset(self):
        user = self.request.user.pk
        queryset = CustomUser.objects.all()
        if self.action != "list": 
            return queryset.filter(pk=user) 
        return queryset
    @action(["get", "put", "patch", "delete"], permission_classes=[IsOwnerProfile], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)
'''