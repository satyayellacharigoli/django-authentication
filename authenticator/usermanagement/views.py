from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import CustomUser
from .serializers import CustomUserSerializer
from .utils import generate_jwt_token, recreate_access_token


class CustomAuthToken(ObtainAuthToken):
    """s
    Login APi
    """
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            tokens = generate_jwt_token(user.id)
            if user:
                user.last_login = timezone.now()
                user.save()
            user_object = CustomUserSerializer(user).data
            return Response(
                {
                    "refresh_token": tokens.get('refresh'),
                    "access_token": tokens.get('access'),
                    "user": user_object
                }, status=status.HTTP_200_OK)
        except ValidationError as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def generate_token(request):
    """
    This API regenerate access token from the refresh_token
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            raise Exception("refresh_token is missing...!")
        tokens = recreate_access_token(refresh_token)
        return Response(tokens, status=status.HTTP_200_OK)
    except Exception as err:
        raise err


class LogoutView(APIView):
    """
    LogoutView
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        This function will clear the user session from the DB.
        """
        request.auth.delete()
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
