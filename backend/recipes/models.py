from django.db import models
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator
from users.models import CustomUser
from ingredients.models import Ingredient
from tags.models import Tag

User = CustomUser

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор рецепта',
                               related_name='recipes')
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиенты',
                            null=True, default = "")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Хэштег',
                            null=True, default = "")
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                    db_index=True)
    text = models.TextField(verbose_name='Описание',
                                   max_length=1000)
    name = models.CharField(max_length=200, verbose_name='Название',
                             null=False)
    image = models.ImageField(upload_to='images/', verbose_name='Изображение', 
                              blank=True, null=True)
    cooking_time = models.CharField( verbose_name='Время готовки в минутах',
                              null=True, validators=[MinValueValidator(1)])
    class Meta:
        ordering = ['-pub_date'] #tags

    def __str__(self):
        return self.name