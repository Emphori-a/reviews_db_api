from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings

from .models import User

from .serializers import UserSignupSerializer, ConfirmationCodeSerializer


class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
            )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)

        if serializer.is_valid():
            # Проверка кода подтверждения и выдача JWT-токена
            user = serializer.user
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)},
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
