from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser

#Форма регистрации


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
