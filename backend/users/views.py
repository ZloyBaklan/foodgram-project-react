from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from djoser.conf import django_settings
from .models import CustomUser

class UserList(APIView):
    def get (self, request, uid):
        user = get_object_or_404(CustomUser, id=request.user.id)
        post_data = {'uid': uid,}
        return Response(post_data)