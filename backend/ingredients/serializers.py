from rest_framework import serializers

from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('__all__')
        lookup_field = 'id'
        extra_kwargs = {'url': {'lookup_field': 'id'}}
