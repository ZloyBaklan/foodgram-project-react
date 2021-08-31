# from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
# from rest_framework.utils import model_meta
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow

User = get_user_model()


class UserFollowSerializer(serializers.ModelSerializer):

    following = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
    )
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Такая подписка уже существует'
            )
        ]

    def validate(self, data):
        if (data['user'] == data['following']
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return FollowListSerializer(
            instance.following,
            context={'request': request}
        ).data


class FollowListSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, user):
        current_user = self.context.get('current_user')
        other_user = user.following.all()
        if user.is_anonymous:
            return False
        if other_user.count() == 0:
            return False
        if Follow.objects.filter(user=user, following=current_user).exists():
            return True
        return False

    def get_recipes(self, obj):
        from recipes.serializers import RecipeImageSerializer
        recipes = obj.recipes.all()[:3]
        request = self.context.get('request')
        return RecipeImageSerializer(
            recipes, many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class CurrentUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_subscribed',
            'username',
            'first_name',
            'last_name',
        #    'password'
        )
        # extra_kwargs = {"password":{'write_only': True}}

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(following=obj, user=user).exists()
