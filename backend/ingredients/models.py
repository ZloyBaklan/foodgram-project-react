from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название ингредиента', null=False)
    measurement_unit = models.CharField(max_length=20,
                                        verbose_name='Единица измерения',
                                        null=False)

    class Meta:
        verbose_name = 'Ингредиент'
        ordering = ['id']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'
