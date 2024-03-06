from rest_framework import serializers
from reviews.models import Comment, Genre, Review, Title

class TitleSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    year = serializers.DateField()
    description = serializers.StringField()
    genre = serializers.SlugRelatedField()
    category = serializers.SlugRelatedField()

    rating = serializers.SerializerMethodField(default=None, read_only=True)
       
    def get_rating(self, obj):
        return self.objects.objects.annotate(
        rating=Avg('reviews__score')).order_by('-year')
    
    class Meta:
        model = Title
        fields = ("id", "name", "year", "rating", "description", "genre", "category")

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
        fields = ("id","text", "author", "score", "pub_date")

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    
    class Meta:
        model = Comment
        fields = ("id","text", "author", "pub_date")
    
