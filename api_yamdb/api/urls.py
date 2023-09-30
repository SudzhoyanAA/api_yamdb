from rest_framework import routers

from django.urls import include, path

from .views import *

app_name = 'api'

api_v1 = routers.DefaultRouter()
api_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(api_v1.urls)),
    path('v1/auth/signup/', UserSignUpViewSet.as_view({'post': 'create'}),
         name='signup'),
    path('v1/auth/token/', UserGetTokenViewSet.as_view({'post': 'create'}),
         name='token')
]
