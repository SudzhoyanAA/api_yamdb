from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from api_yamdb.constants import MAX_USERNAME_LENGHT, MAX_EMAIL_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title

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
        fields = ('__all__')


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
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
        default=GetDefaultTitleId()
    )

    class Meta:
        model = Review
        fields = ('__all__')
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
        fields = ('__all__')


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=MAX_USERNAME_LENGHT,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')]
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_EMAIL_LENGTH,
    )

    def validate_email(self, data):
        if data is None or data == '':
            raise serializers.ValidationError('Вы не указали email')
        return data

    def validate_username(self, data):
        if data == 'me':
            raise ValidationError('Нельзя использовать "me" в '
                                  'качестве имени пользователя')
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class UserTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True,
                                     max_length=MAX_USERNAME_LENGHT)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound('Указанное имя не найдено')
        return value


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
