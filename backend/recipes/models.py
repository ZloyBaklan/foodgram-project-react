from django.db import models
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator
from users.models import CustomUser
from ingredients.models import Ingredient
from tags.models import Tag
from django.db.models import UniqueConstraint

User = CustomUser

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор рецепта',
                               related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, 
                                         verbose_name='Ингредиенты')
    tag = models.ManyToManyField(Tag, verbose_name='Хэштег',
                            null=True, default = "")
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                    db_index=True)
    text = models.TextField(verbose_name='Описание',
                                   max_length=1000)
    name = models.CharField(max_length=200, verbose_name='Название',
                             null=False)
    image = models.ImageField(upload_to='images/', verbose_name='Изображение', 
                              blank=True, null=True)
    cooking_time = models.IntegerField(default=0, verbose_name='Время готовки в минутах',
                              blank=True, validators=[MinValueValidator(1)])
    class Meta:
        ordering = ['-pub_date'] #tags

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
    class Meta:
        UniqueConstraint(fields=['favorite', 'user'], name='favorite_unique')

    def __str__(self):
        return f"{self.user} has favorites: {self.favorite.name}"

class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользоавтель')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Покупка')
    def __str__(self):
        return f'In {self.user} shopping list: {self.recipe}'

class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, 
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name= 'Рецепт', related_name='recipes_ingredients_list'
    )
    amount = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)],
        verbose_name='Количество ингредиентов'
    )
    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'