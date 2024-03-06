from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.views import APIView

from django.contrib.auth.tokens import default_token_generator
from api_yamdb import settings
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from .serializers import (UserSignupSerializer,
                          ConfirmationCodeSerializer,
                          UserProfileSerializer)

User = get_user_model()


class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            User.objects.create_user(
                username=username,
                email=email,
            )

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

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )

        if default_token_generator.check_token(
                user,
                serializer.validated_data['confirmation_code']
        ):
            token = AccessToken.for_user(user).get('jti')
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            resp = {'confirmation_code': 'Неверный код подтверждения'}
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
