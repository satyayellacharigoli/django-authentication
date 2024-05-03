"""
Utils Module
"""
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser


def generate_jwt_token(user_id):
    """
    This function will generate JWT Token
    """
    user = CustomUser.objects.get(id=user_id)
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def recreate_access_token(refresh_token):
    """
    This function will recreate the access token using the provided refresh token.
    """
    try:
        refresh_token = RefreshToken(refresh_token)
        return {
            'refresh_token': str(refresh_token),
            'access_token': str(refresh_token.access_token),
        }
    except Exception as err:
        raise err
