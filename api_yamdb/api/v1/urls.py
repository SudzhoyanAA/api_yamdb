from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.v1.views import (
    CategoryViewSet, GenreViewSet, TitleViewSet,
    CommentViewSet, ReviewViewSet,
    UserSignUpAPIView,
    UserViewSet, UserGetTokenAPIView
)

api_v1 = DefaultRouter()
api_v1.register(r'categories', CategoryViewSet, basename='category')
api_v1.register(r'genres', GenreViewSet, basename='genre')
api_v1.register(r'titles', TitleViewSet, basename='title')
api_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
api_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
api_v1.register(r'users', UserViewSet, basename='users')

api_v1.auth = [
    path('signup/', UserSignUpAPIView.as_view(), name='signup'),
    path('token/', UserGetTokenAPIView.as_view(), name='token'),

]
urlpatterns = [
    path('', include(api_v1.urls)),
    path('auth/', include(api_v1.auth)),
]
