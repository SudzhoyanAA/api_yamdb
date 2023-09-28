from rest_framework import viewsets
from users.models import User
from api.serializers import UserSerializer
from api.permissions import (IsAdminPermissions,
                             IsAuthenticated,
                             IsOnlyAdminPermissions,
                             IsAdminOrAuthorOrModeratorPermissions
                             )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
