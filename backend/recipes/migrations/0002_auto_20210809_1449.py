# Generated by Django 3.2.6 on 2021-08-09 11:49

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_alter_tag_color'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='tags.tag', verbose_name='Хэштег'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.IntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время готовки в минутах'),
        ),
    ]
