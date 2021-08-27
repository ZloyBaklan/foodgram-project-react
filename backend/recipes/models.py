from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from ingredients.models import Ingredient
from tags.models import Tag
from users.models import CustomUser

User = CustomUser


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор рецепта',
                               related_name='author')
    ingredients = models.ManyToManyField(Ingredient, 
                                         related_name='ingredients', 
                                         through='IngredientAmount',
                                         verbose_name='Ингредиенты')
    tag = models.ManyToManyField(Tag, related_name='tags', verbose_name='Хэштег')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                    db_index=True)
    text = models.TextField(verbose_name='Описание',
                            max_length=1000)
    name = models.CharField(max_length=200, verbose_name='Название',
                            null=False)
    image = models.ImageField(upload_to='media/', verbose_name='Изображение',
                              blank=True, null=True)
    cooking_time = models.IntegerField(
        default=0, verbose_name='Время готовки в минутах',
        blank=True, validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Рецепт'
        ordering = ['-pub_date']  # tags

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites',
                             on_delete=models.CASCADE)
    favorite = models.ForeignKey(Recipe, related_name='favorites',
                                 on_delete=models.CASCADE)

    class Meta:
        UniqueConstraint(fields=['favorite', 'user'], name='favorite_unique')

    def __str__(self):
        return f"{self.user} has favorites: {self.favorite.name}"


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_shopping_list',
                             verbose_name='Пользоавтель')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='purchases',
                               verbose_name='Покупка')
    added_time = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления'
    )

    def __str__(self):
        return f'In {self.user} shopping list: {self.recipe}'


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='ingredients_in_recipe', verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipes_ingredients_list', verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)],
        verbose_name='Количество ингредиентов'
    )

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'
