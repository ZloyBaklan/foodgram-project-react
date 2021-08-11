from rest_framework import serializers
from .models import CustomUser, Follow
from rest_framework.validators import UniqueTogetherValidator
from djoser.serializers import UserCreateSerializer

User = CustomUser

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
    '''
    def representation(self, instance):
        request = self.context.get('request')
        return ShowFollowerSerializer(
            instance.following,
            context={'request':request}
        ).data
    '''

class FollowListSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    count_recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = '__all__'
    
    def get_is_subscribed(self, user):
        current = self.context.get('current')
        other = current.following.all()
        if user.is_anonymous:
            return False
        if other.count()==0:
            return False
        if Follow.objects.filter(user=user, following=current).exists():
            return True
        return False
    '''
    def get_recipes(self, obj):
        from recipes.serializers import ShowRecipeAddedSerializer
        recipes = obj.recipes.all()[:settings.RECIPES_LIMIT]
        request = self.context.get('request')
        return ShowRecipeAddedSerializer(
            recipes, many = True,
            context={'request': request}
        ).data
    def get_recipes_count(self, obj):
        return obj.recipes.count()
    '''
class CurrentUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'is_subscribed', 
                  'first_name','last_name')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(following=obj, user=user).exists()



class userProfileSerializer(serializers.ModelSerializer):
    user=CurrentUserSerializer(read_only=True)
    class Meta:
        model=CustomUser
        fields='__all__'
