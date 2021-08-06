from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название тега',
                             null=False)
    slug = models.SlugField(verbose_name='Ссылка', unique=True,
                            help_text='Ссылка тега')
    color = models.TextField(verbose_name='Описание группы',
                                   max_length=300)

    def __str__(self):
        return self.name