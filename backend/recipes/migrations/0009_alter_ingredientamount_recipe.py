# Generated by Django 3.2.6 on 2021-08-12 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20210812_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_ingredients_list', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
