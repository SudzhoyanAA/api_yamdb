from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = User
        fields = '__all__'
