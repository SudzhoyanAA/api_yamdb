from django.core.validators import RegexValidator
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from api_yamdb.constants import MAX_USERNAME_LENGHT, MAX_EMAIL_LENGHT
from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Title
        fields = '__all__'


class GetDefaultTitleId:
    requires_context = True

    def __call__(self, serializer_field):
        return (serializer_field.context['request']
                .parser_context['kwargs']['title_id'])


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault(),
    )
# если убрать это поле то падают тесты о корректности данных
# (так же и с коментами).
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
        default=GetDefaultTitleId()
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('author',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Нельзя повторно оценить произведение.'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=MAX_USERNAME_LENGHT,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')]
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_EMAIL_LENGHT,
    )

    class Meta:
        model = User
        fields = ['email', 'username']

    # def validate(self, data):
    #     """Запрещает пользователям присваивать себе имя me
    #     и использовать повторные username и email."""
    #     if data.get('username') == 'me':
    #         raise serializers.ValidationError(
    #             'Использовать имя me запрещено'
    #         )
    #     if User.objects.filter(username=data.get('username')):
    #         raise serializers.ValidationError(
    #             'Пользователь с таким username уже существует'
    #         )
    #     if User.objects.filter(email=data.get('email')):
    #         raise serializers.ValidationError(
    #             'Пользователь с таким email уже существует'
    #         )
    #     return data

    def create(self, validated_data):
        try:
            user = User.objects.get_or_create(**validated_data)[0]
        except IntegrityError:
            raise ValidationError(
                'Отсутствует обязательное поле или оно некоректно',
            )
        return user

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использование данного имени запрещено!'
            )
        return value


class UserTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True,
                                     max_length=MAX_USERNAME_LENGHT)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
