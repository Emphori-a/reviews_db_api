from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth import get_user_model

from .serializers import UserSignupSerializer, ConfirmationCodeSerializer, \
    UserProfileSerializer
from .permissions import IsAdmin

User = get_user_model()


def send_email(username, email):
    user = User.objects.get(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)

    mail_subject = f'Код подтверждения для пользователя {username}'
    message = f'Ваш {mail_subject.lower()}: {confirmation_code}'
    sender_email = settings.DEFAULT_FROM_EMAIL
    recipient_email = email
    send_mail(
        mail_subject,
        message,
        sender_email,
        [recipient_email],
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

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']

        User.objects.create_user(username=username, email=email)
        send_email(username=username, email=email)
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

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

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

        token = AccessToken.for_user(user).get('jti')
        return Response({'token': token}, status=status.HTTP_200_OK)


class UserProfile(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    permission_classes = [IsAdmin | IsAdminUser]
    search_fields = ('user__username',)







