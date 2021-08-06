from django.db import models
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()
class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор поста',
                               related_name='posts')
    ingredients = models.CharField(max_length=200, verbose_name='Ингредиенты',
                             null=False)
    #tags = TaggableManager()
    text = models.TextField(verbose_name='Описание',
                                   max_length=1000)
    name = models.CharField(max_length=200, verbose_name='Название',
                             null=False)
    image = models.ImageField(upload_to='images/', verbose_name='Изображение', 
                              blank=True, null=True)
    cooking_time = models.CharField(max_length=200, 
                              verbose_name='Время готовки в минутах',
                              null=False, validators=[MinValueValidator(1)])


    def __str__(self):
        return self.name