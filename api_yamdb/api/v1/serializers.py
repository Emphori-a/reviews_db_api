from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Comment, Category, Genre, Review, Title
from api_yamdb.settings import MAX_LENGTH_USER, MAX_LENGTH_EMAIL
from user.validators import validate_username_not_me, validate_username_symbols


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True, default=None)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'rating',
                  'genre', 'category')


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True,
        allow_null=True, allow_empty=False)

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
        slug_field='username',
    )

    def validate(self, attrs):
        if self.context['request'].method != 'POST':
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
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USER,
        validators=[validate_username_not_me, validate_username_symbols]
    )
    email = serializers.EmailField(max_length=MAX_LENGTH_EMAIL)

    def validate(self, data):
        existing_user_by_username = User.objects.filter(
            username=data['username']).first()
        existing_user_by_email = User.objects.filter(
            email=data['email']).first()

        if existing_user_by_username != existing_user_by_email:
            error_msg = {}
            if existing_user_by_username:
                error_msg[
                    'username'] = ('Пользователь с таким '
                                   'username уже существует.')
            if existing_user_by_email:
                error_msg['email'] = ('Пользователь с таким '
                                      'email уже существует.')
            raise serializers.ValidationError(error_msg)

        return data

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email'])
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            f'Код подтверждения для пользователя {user.username}',
            f'Ваш Код подтверждения для пользователя {user.username}: '
            f'{confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )
        return user


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=MAX_LENGTH_USER)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        if not data.get('username'):
            raise serializers.ValidationError("Нет данных в запросе!")

        user = get_object_or_404(User, username=data.get('username'))
        # code = data.get('confirmation_code')

        if not default_token_generator.check_token(
                user,
                data.get('confirmation_code')
        ):
            raise serializers.ValidationError('Неверный код подтверждения')

        return {'token': str(AccessToken.for_user(user))}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }
