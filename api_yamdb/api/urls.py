from django.urls import include, path
from rest_framework import routers

from rest_framework.authtoken import views

from .views import UsersViewSet

api_v1 = routers.DefaultRouter()
# api_v1.register('auth', UserViewSet, basename='user')
api_v1.register(r'users', UsersViewSet, basename='users')


urlpatterns = [
    path('v1/', include(api_v1.urls)),
    #path('v1/api-token-auth/', views.obtain_auth_token),
    # path('v1/auth/token/', include('djoser.urls'), name='signup'),
    #path('v1/auth/signup/', UsersViewSet),
    path('v1/auth/signup/', UsersViewSet),
]
