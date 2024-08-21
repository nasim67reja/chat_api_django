# users/views.py

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from users.serializers import SignupSerializer, SigninSerializer, UserSerializer
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user_data = UserSerializer(user).data
            token = RefreshToken.for_user(user=user)
            return Response(
                {
                    "idToken": str(token.access_token),
                    "refreshToken": str(token),
                    "user": user_data,
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Signup failed: {e}", exc_info=True)
            return Response(
                {"error": "Signup failed", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class SigninView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = SigninSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = User.objects.get(username=username)
            if user.check_password(password):
                user_data = UserSerializer(user).data
                token = RefreshToken.for_user(user=user)
                return Response(
                    {
                        "idToken": str(token.access_token),
                        "refreshToken": str(token),
                        "user": user_data,
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Wrong Credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except User.DoesNotExist:
            return Response(
                {"error": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Signin failed: {e}", exc_info=True)
            return Response(
                {"error": "An unexpected error occurred", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            user_data = UserSerializer(user).data
            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"User detail retrieval failed: {e}", exc_info=True)
            return Response(
                {"error": "Failed to retrieve user details", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"User update failed: {e}", exc_info=True)
            return Response(
                {"error": "Failed to update user details", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            user.is_deleted = True
            user.save()
            return Response(
                {"message": "User account deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            logger.error(f"User deletion failed: {e}", exc_info=True)
            return Response(
                {"error": "Failed to delete user account", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
