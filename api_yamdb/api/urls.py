from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet,
    CommentViewSet, ReviewViewSet, UserGetTokenViewSet,
    UserSignUpViewSet, UserViewSet
)

api_v1 = DefaultRouter()
api_v1.register(r'categories', CategoryViewSet)
api_v1.register(r'genres', GenreViewSet)
api_v1.register(r'titles', TitleViewSet)
api_v1.register(r'titles', TitleViewSet)
api_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
api_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
api_v1.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(api_v1.urls)),
    path('v1/auth/signup/', UserSignUpViewSet.as_view({'post': 'create'}),
         name='signup'),
    path('v1/auth/token/', UserGetTokenViewSet.as_view({'post': 'create'}),
         name='token')
]
