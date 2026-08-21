from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from .serializers import (ForgotPasswordSerializer, ResetPasswordSerializer,)
from .serializers import TrainingCoordinatorLoginSerializer


class TrainingCoordinatorLoginAPIView(APIView):

    def post(self, request):

        serializer = TrainingCoordinatorLoginSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login Successful",

                "access": str(refresh.access_token),

                "refresh": str(refresh),

                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            },
            status=status.HTTP_200_OK
        )

class ForgotPasswordAPIView(APIView):

    def post(self, request):

        serializer = ForgotPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data["email"]

        user = User.objects.get(email=email)

        token = default_token_generator.make_token(user)

        reset_link = (
            f"http://localhost:3000/reset-password/"
            f"{user.id}/{token}"
        )

        send_mail(
            subject="Password Reset",
            message=f"Click the link below:\n\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response(
            {
                "message": "Password reset link sent successfully."
            }
        )
    

class ResetPasswordAPIView(APIView):

    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            return Response(
                {
                    "error": "Invalid User"
                },
                status=404,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {
                    "error": "Invalid or Expired Token"
                },
                status=400,
            )

        user.set_password(password)
        user.save()

        return Response(
            {
                "message": "Password updated successfully."
            }
        )