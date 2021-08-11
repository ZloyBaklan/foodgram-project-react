
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

#from .models import CustomUser
from django.db.models import UniqueConstraint



class CustomUser(AbstractUser):

    username = models.CharField(
        verbose_name="Логин", unique=True, max_length=100
    )

    email = models.EmailField(verbose_name="Email", null=False, unique=True)

    first_name = models.TextField(
        verbose_name="Имя", max_length=100, blank=True
    )
    last_name = models.TextField(
        verbose_name="Фамилия", max_length=100, blank=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.email

User = CustomUser

class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Подписка',
                               related_name='following')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Подписчик',
                             related_name='follower')

    class Meta:
        UniqueConstraint(fields=['following', 'user'], name='follow_unique')

    def __str__(self):
        return f"{self.user} follows {self.following}"
