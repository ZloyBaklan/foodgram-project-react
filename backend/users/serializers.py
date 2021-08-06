from rest_framework import serializers
from .models import CustomUser, Follow
from rest_framework.validators import UniqueTogetherValidator
from djoser.serializers import UserCreateSerializer

User = CustomUser

class UserFollowSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField( 
        slug_field='username', 
        queryset=User.objects.all(), 
    ) 
    user = serializers.SlugRelatedField( 
        slug_field='username', 
        queryset=User.objects.all(), 
        default=serializers.CurrentUserDefault() 
    ) 
 
    class Meta: 
        fields = '__all__' 
        model = Follow 
        validators = [ 
            UniqueTogetherValidator( 
                queryset=Follow.objects.all(), 
                fields=('user', 'author'), 
                message='Такая подписка уже существует' 
            ) 
        ] 
 
    def validate(self, data): 
        if (data['user'] == data['author'] 
                and self.context['request'].method == 'POST'): 
            raise serializers.ValidationError( 
                'Нельзя подписаться на самого себя' 
            ) 
        return data

'''
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'first_name',
            'last_name', 'username', 
            'email', 'id',
        )
        model = CustomUser
'''
class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'first_name','last_name')

class userProfileSerializer(serializers.ModelSerializer):
    user=CurrentUserSerializer(read_only=True)
    class Meta:
        model=CustomUser
        fields='__all__'

