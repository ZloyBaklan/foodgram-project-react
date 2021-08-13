from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from ingredients.models import Ingredient
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from tags.models import Tag
from users.serializers import CurrentUserSerializer

from .models import Favorite, IngredientAmount, Recipe, ShoppingList


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient',
                                            read_only=True)
    name = serializers.SlugRelatedField(slug_field='name',
                                        source='ingredient', read_only=True)
    measurement_unit = serializers.SlugRelatedField(
        slug_field='measurement_unit',
        source='ingredient', read_only=True
        )

    class Meta:
        model = IngredientAmount
        fields = '__all__'


class AddToIngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient',
                                            queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        IngredientAmount
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    tag = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    ingredients = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = ('__all__')
        model = Recipe

    def get_ingredients(self, obj):
        recipe = obj
        queryset = recipe.recipes_ingredients_list.all()
        return IngredientAmountSerializer(queryset, many=True).data

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Favorite.objects.filter(favorite=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return ShoppingList.objects.filter(recipe=obj, user=user).exists()


class RecipeImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_url(obj.image.url)


class RecipeFullSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True)
    author = CurrentUserSerializer(read_only=True)
    ingredients = AddToIngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def create_bulk(self, recipe, data):
        IngredientAmount.objects.bulk_create([IngredientAmount(
            ingredient=ingredient['ingredient'],
            recipe=recipe,
            amount=ingredient['amount']
        ) for ingredient in data])

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.save()
        recipe.tags.set(tags)
        self.create_bulk(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.create_bulk(instance, ingredients)
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        instance.cooking_time = validated_data.pop('cooking_time')
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')
        instance.save()
        instance.tags.set(tags)
        return instance

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError({
                    'ingredients': ('Число игредиентов должно быть больше 0')
                })
        return data

    def validate_cooking_time(self, data):
        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше 0'
            )

    def to_representation(self, instance):
        data = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'favorite'),
                message='Рецепт уже добавлен в избранное'
            )
        ]

    def to_representation(self, instance):
        requset = self.context.get('request')
        return RecipeImageSerializer(
            instance.recipe,
            context={'request': requset}
        ).data


class ShoppingListSerializer(FavoriteSerializer):
    class Meta(FavoriteSerializer.Meta):
        model = ShoppingList
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в список покупок'
            )
        ]

    def to_representation(self, instance):
        requset = self.context.get('request')
        return RecipeImageSerializer(
            instance.recipe,
            context={'request': requset}
        ).data
