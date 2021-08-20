from colorfield.fields import ColorField
from django.db import models


class Tag(models.Model):
    COLOR_CHOICES = [
        ("#FFFFFF", "white"),
        ("#000000", "black"),
        ("#00FF00", "green"),
        ("#FF00FF", "pink panther"),
        ("#FF9900", "orange"),
        ("#CC0000", "cherry"),
        ("#CC00FF", "purple"),

    ]
    name = models.CharField(max_length=200, verbose_name='Название тега',
                            null=False)
    slug = models.SlugField(verbose_name='Ссылка', unique=True,
                            help_text='Ссылка тега')
    color = ColorField(choices=COLOR_CHOICES, verbose_name='Цвет тэга')

    class Meta:
        verbose_name = 'Тэг'

    def __str__(self):
        return self.name
