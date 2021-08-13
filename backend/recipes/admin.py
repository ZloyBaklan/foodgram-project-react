from django.contrib import admin 
from .models import Favorite, Recipe

admin.site.register(Recipe)
admin.site.register(Favorite)