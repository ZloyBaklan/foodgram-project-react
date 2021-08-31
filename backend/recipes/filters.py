import django_filters as filters

from .models import Recipe, Ingredient
from tags.models import Tag


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        qs = queryset.filter(is_favorited=value)
        return qs

    def is_in_shopping_cart_filter(self, queryset, name, value):
        qs = queryset.filter(is_in_shopping_cart=value)
        return qs


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name', )
