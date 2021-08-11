from rest_framework import serializers

from ingredients.serializers import IngredientSerializer
from .models import Favorite, Recipe
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
class CurrentUserSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    class Meta:
        model = Recipe
        fields = ('__all__')

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Favorite.objects.filter(recipe=obj, user=user).exists()