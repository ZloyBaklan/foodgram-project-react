from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from tags.models import Tag
from users.models import CustomUser

User = CustomUser


class Ingredient(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название ингредиента', null=False)
    measurement_unit = models.CharField(max_length=20,
                                        verbose_name='Единица измерения',
                                        null=False)

    class Meta:
        verbose_name = 'Ингредиент'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор рецепта',
                               related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='ingredients',
                                         through='IngredientAmount',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, related_name='tags',
                                  verbose_name='Хэштег')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                    db_index=True)
    text = models.TextField(verbose_name='Описание',
                            max_length=1000)
    name = models.CharField(max_length=200, verbose_name='Название',
                            null=False)
    image = models.ImageField(upload_to='media/', verbose_name='Изображение')
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1, 'Значение не может быть меньше 1')],
        verbose_name='Время готовки в минутах',
    )

    class Meta:
        verbose_name = 'Рецепт'
        ordering = ['-pub_date']  # tags

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='favorites',
                               on_delete=models.CASCADE)
    added = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления в избранное'
    )

    class Meta:
        verbose_name = 'Избранное'
        UniqueConstraint(fields=['recipe', 'user'], name='favorite_unique')

    def __str__(self):
        return f"{self.user} has favorites: {self.recipe.name}"


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_shopping_list',
                             verbose_name='Пользоавтель')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='purchases',
                               verbose_name='Покупка')
    added = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления в список покупок'
    )

    class Meta:
        verbose_name = 'Покупки'

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

    class Meta:
        verbose_name = 'Количество'

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'
