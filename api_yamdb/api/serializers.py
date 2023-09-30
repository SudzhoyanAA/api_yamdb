from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')],
    )
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        fields = ('email', 'username')
        model = User

    # # # Проверить это условие Что-то не так

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использование данного имени запрещено!'
            )
        return value


class UserTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)


class UserGetTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(read_only=True,
                                            slug_field='username')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserMeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
