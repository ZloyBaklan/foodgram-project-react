from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'confirmation_code', 'first_name',
            'last_name', 'username', 'bio', 'email', 'role',
        )
        model = CustomUser


class ConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
