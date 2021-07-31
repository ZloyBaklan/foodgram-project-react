from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):

    class UserRoles(models.TextChoices):
        CUSTOMUSER = 'user', _('user')
        ADMIN = 'admin', _('admin')

    username = models.CharField(
        verbose_name="Логин", unique=True, max_length=100
    )

    email = models.EmailField(verbose_name="Email", null=False, unique=True)

    role = models.CharField(
        verbose_name="Права(установлены админом)",
        choices=UserRoles.choices, default=UserRoles.CUSTOMUSER, max_length=15
    )
    first_name = models.TextField(
        verbose_name="Имя", max_length=100, blank=True
    )
    last_name = models.TextField(
        verbose_name="Фамилия", max_length=100, blank=True
    )
    confirmation_code = models.CharField(max_length=10, default='0000000000')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.email

    @property
    def is_upperclass(self):
        return self.role in (self.UserRoles.ADMIN)
