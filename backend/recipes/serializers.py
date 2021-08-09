from rest_framework import serializers

from ingredients.serializers import IngredientSerializer
from .models import Recipe
from ingredients.models import Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    tag = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        fields = ('__all__')
        model = Recipe
'''       
    def create(self, validated_data):
        ingredient_validated_data = validated_data.pop('ingredients')
        ingredient = Ingredient.objects.create(**validated_data)
        ingredient_set_serializer = self.fields['ingredients']
        for each in ingredient_validated_data:
            each['ingredient'] = ingredient
        choices = ingredient_set_serializer.create(ingredient_validated_data)
        return ingredient
'''