from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.settings import ADMIN_EMAIL

from .models import CustomUser
from .permissions import IsAdmin, IsOwnerProfile
from .serializers import (ConfirmationSerializer, SendCodeSerializer,
                          UserSerializer)


class CreateUserViewSet(viewsets.ModelViewSet):
   # permission_classes = [IsAdmin]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsOwnerProfile],
    )
    def me(self, request):
        user = get_object_or_404(CustomUser, id=request.user.id)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
        else:
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = SendCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    user = (
        CustomUser.objects.get_or_create(
            email=email, username=request.user.username
        )
    )
    confirmation_code = default_token_generator.make_token(user)
    CustomUser.objects.filter(user=user).update(
        confirmation_code=make_password(
            confirmation_code, salt=None, hasher='default'
        )
    )
    mail_subject = 'Код подтверждения'
    message = f'Код подтверждения регистрации: {confirmation_code}'
    send_mail(mail_subject, message, f'FOODGRAM {ADMIN_EMAIL}', [email])
    return Response(
        f'Код отправлен на адрес {email}', status=status.HTTP_200_OK
    )


@api_view(['POST'])
def get_jwt_token(request):
    serializer = ConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(CustomUser, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST)
