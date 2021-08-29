from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField('email', null=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    # objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ['id']

    def __str__(self):
        return f'Пользователь {self.email}'


User = CustomUser


class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  verbose_name='Подписка',
                                  related_name='following')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Подписчик',
                             related_name='follower')

    class Meta:
        verbose_name = 'Подписки'
        UniqueConstraint(fields=['following', 'user'], name='follow_unique')

    def __str__(self):
        return f"{self.user} follows {self.following}"
