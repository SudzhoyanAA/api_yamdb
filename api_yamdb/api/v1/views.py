from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView

from reviews.models import Category, Genre, Review, Title
from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet, ExcludePutViewSet
from .permissions import (IsAdmin, IsAdminModeratorOwnerOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, TitleReadSerializer,
                          ReviewSerializer, TitleSerializer,
                          UserSerializer, UserTokenSerializer,
                          UserSignUpSerializer, UserTokenSerializer)
from .utils import send_message_to_user

User = get_user_model()


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


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
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
        )


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


class UserSignUpAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    # queryset = User.objects.all()

    def post(self, queryset):
        if User.objects.filter(
            username=queryset.data.get('username'),
            email=queryset.data.get('email')
        ).exists():
            return Response(queryset.data, status=status.HTTP_200_OK)
        serializer = UserSignUpSerializer(data=queryset.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        send_message_to_user(user.username, user.email, confirmation_code)
        return Response(serializer.data)

    # def post(self, queryset):
    #     serializer = UserSignUpSerializer(data=queryset.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     user = User.objects.get(email=queryset.data["email"])
    #     confirmation_code = default_token_generator.make_token(user)
    #     send_message_to_user(user.username, user.email, confirmation_code)
    #     return Response(serializer.data)


class UserGetTokenAPIView(APIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        if default_token_generator.check_token(
                username, serializer.data['confirmation_code']
        ):
            token = AccessToken.for_user(username)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ExcludePutViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get'],
        url_path='me',
        url_name='me',
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        serializer = UserSerializer(
            self.request.user
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @me.mapping.patch
    def me2(self, request):
        serializer = UserSerializer(
            self.request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=self.request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
