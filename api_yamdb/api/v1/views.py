from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, status
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
from .utils import send_message_to_user, make_confirmation_code

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

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        if User.objects.filter(username=username, email=email).exists():
            send_message_to_user(username, email, make_confirmation_code(
                get_object_or_404(User, username=username)))
            return Response(request.data, status=status.HTTP_200_OK)
        if ((User.objects.filter(email=email).exists()
             and not User.objects.filter(username=username).exists())
                or (User.objects.filter(username=username).exists()
                    and User.objects.filter(email=email) != email)):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_message_to_user(username, email,
                             make_confirmation_code(serializer.save()))
        return Response(request.data, status=status.HTTP_200_OK)


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
    def me_get(self, request):
        serializer = UserSerializer(
            self.request.user
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @me_get.mapping.patch
    def me_patch(self, request):
        serializer = UserSerializer(
            self.request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=self.request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
