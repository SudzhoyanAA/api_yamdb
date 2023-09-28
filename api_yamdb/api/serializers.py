from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from overview.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

        read_only_fields = ('author',)

    def validate(self, data):
        user = self.context['request'].user
        existing_review = Review.objects.filter(author=user).first()
        if existing_review:
            raise ValidationError("Вы уже добавили отзыв")

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

        read_only_fields = ('author',)
