from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Comment, Category, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')
        model = Title

    def get_rating(self, obj):
        return None
    # в таком виде не работает, убрала пока
        # return self.objects.objects.annotate(
        #     rating=Avg('reviews__score')).order_by('-year')


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')
        model = Title

    def to_representation(self, instance):
        serializer = TitleSerializer(instance)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, attrs):
        if not self.context['request'].method == 'POST':
            return attrs
        if Review.objects.filter(
            title_id=self.context['view'].kwargs.get('title_id'),
            author=self.context['request'].user,
        ).exists():
            raise serializers.ValidationError(
                (
                    'Пользователь может оставлять отзыв на каждое произведение'
                    'не более одного раза'
                )
            )
        return attrs

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
