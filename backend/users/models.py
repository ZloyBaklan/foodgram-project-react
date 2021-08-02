from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


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


    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.email
