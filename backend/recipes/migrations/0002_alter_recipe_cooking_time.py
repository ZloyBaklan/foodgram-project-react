# Generated by Django 3.2.6 on 2021-08-31 09:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(blank=True, default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время готовки в минутах'),
        ),
    ]
