from rest_framework import serializers

from reviews.models import Category, Genre, Title


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

    # здесь нужно дописать логику расчета рейтинга
    # Если отзывов о произведении нет - 'значением поля должено быть `None
    def get_rating(self, obj):
        return obj.reviews.all().count()

    # def validate_category(self, value):
    #     if value not in Category.objects.all().values('slug'):
    #         raise serializers.ValidationError(
    #             'Можно указать только существующую категорию')
    #     return Category.objects.all().filter('slug')
