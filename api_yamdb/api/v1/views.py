from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.conf.global_settings import DEFAULT_FROM_EMAIL

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Review, Title
from user.models import User
from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet, ExcludePutViewSet
from .permissions import (IsAdmin, IsAdminModeratorOwnerOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, TitleReadSerializer,
                          ReviewSerializer, TitleSerializer,
                          UserSerializer, UserTokenSerializer,
                          UserSignUpSerializer, UserTokenSerializer)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
# в Django REST framework (DRF) используется для определения поля, которое
# будет использоваться для поиска объектов в представлениях. Это поле
# позволяет задать, какое поле модели будет использоваться для поиска
# объектов, когда вы выполняете запросы на просмотр (retrieve), обновление
# (update), частичное обновление (partial update), удаление (delete) и
# другие действия на основе идентификационного значения.
# Поискал альтернативу, но не нашел. И почему это костыль?


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ExcludePutViewSet):
    queryset = Title.objects.order_by('id').annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(ExcludePutViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ExcludePutViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


def send_message_to_user(username, recepient_email, confirmation_code):
    send_mail(
        subject='Код подтверждения YAMDb',
        message=f'Здравствуйте, {username} \n\n'
                f'Вы получили это сообщение, '
                f'так как на адрес электронной почты: \n'
                f' {recepient_email}\n'
                f'происходит регистрация на сайте "API_yamdb". \n  \n'
                f'Ваш код подтверждения : {confirmation_code} \n \n'
                f'Если Вы не пытались зарегистрироваться - \n'
                f'просто не отвечайте на данное сообщение и \n'
                f'не производите никаких действий',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=(recepient_email,),
    )


class UserSignUpAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=request.data["email"])
        confirmation_code = default_token_generator.make_token(user)
        send_message_to_user(user.username, user.email, confirmation_code)
        return Response(serializer.data)


class UserGetTokenAPIView(APIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=request.data['username']
        )
        if default_token_generator.check_token(
                user, serializer.data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        raise ValidationError("Неверный код")


class UserViewSet(ExcludePutViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            self.request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=self.request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
