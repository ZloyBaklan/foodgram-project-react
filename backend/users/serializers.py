from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.utils import model_meta
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
        fields = '__all__'

    def get_is_subscribed(self, user):
        current = self.context.get('current')
        other = current.following.all()
        if user.is_anonymous:
            return False
        if other.count() == 0:
            return False
        if Follow.objects.filter(user=user, following=current).exists():
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


class CurrentUserSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(following=obj, user=user).exists()

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            # username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
'''    
    def create(self, validated_data):
        serializers.raise_errors_on_nested_writes('create',
                                                  self, validated_data)
        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)
        try:
            instance = ModelClass._default_manager.create_user(
                **validated_data
            )
        except TypeError:
            ('Unexpected type of tagged object')
'''


class UserProfileSerializer(serializers.ModelSerializer):
    user = CurrentUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
