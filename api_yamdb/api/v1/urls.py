from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rest_framework import routers

from api.v1.views import (
    CategoryViewSet, GenreViewSet, TitleViewSet,
    CommentViewSet, ReviewViewSet, UserGetTokenViewSet,
    UserSignUpViewSet, UserViewSet
)

api_v1 = DefaultRouter()
api_v1.register(r'categories', CategoryViewSet)
api_v1.register(r'genres', GenreViewSet)
api_v1.register(r'titles', TitleViewSet)
api_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
api_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
api_v1.register(r'users', UserViewSet, basename='users')

auth_router_v1 = routers.SimpleRouter()
# auth_router_v1.register(r"signup", UserSignUpViewSet, basename="signup")
auth_router_v1.register(r"signup", UserSignUpViewSet, basename="signup")
auth_router_v1.register(r"token", UserGetTokenViewSet, basename="token")

urlpatterns = [
    path('', include(api_v1.urls)),
    path("auth/", include(auth_router_v1.urls)),
    # path('auth/signup/', UserSignUpViewSet.as_view({'post': 'create'}),
    #      name='signup'),
    # path('auth/token/', UserGetTokenViewSet.as_view({'post': 'create'}),
    #      name='token')
]
