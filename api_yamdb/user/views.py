from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsOwnerOrIsAdmin
from .serializers import (UserSignupSerializer,
                          ConfirmationCodeSerializer,
                          UserProfileSerializer)
from api.mixins import PutNotAllowed


User = get_user_model()


def send_email(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        f'Код подтверждения для пользователя {user.username}',
        f'Ваш Код подтверждения для пользователя {user.username}: '
        f'{confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False
    )


class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')

        if User.objects.filter(username=username, email=email).exists():
            return Response('Вы уже зарегистрированы!',
                            status=status.HTTP_200_OK)

        if User.objects.filter(email=email).exists() or User.objects.filter(
                username=username).exists():
            return Response('Такой пользователь уже зарегистрирован',
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(username=username, email=email)
        send_email(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)

        if not request.data.get('username'):
            return Response("Нет данных в запросе!",
                            status=status.HTTP_400_BAD_REQUEST)

        username = request.data.get('username')
        if not User.objects.filter(username=username).exists():
            return Response('Пользователь не найден',
                            status=status.HTTP_404_NOT_FOUND)

        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )

        if not default_token_generator.check_token(
                user,
                serializer.validated_data['confirmation_code']
        ):
            resp = {'confirmation_code': 'Неверный код подтверждения'}
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)

        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserProfileSet(viewsets.ModelViewSet, PutNotAllowed):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrIsAdmin]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        url_path='me',
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated]
    )
    def get_user_selfpage(self, request):
        if request.method == 'GET':
            serializer = UserProfileSerializer(request.user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
