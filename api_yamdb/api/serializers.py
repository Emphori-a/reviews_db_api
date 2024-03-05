from rest_framework import serializers
from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "author", "text", "score", "pub_date", "title")

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "review", "text", "created")