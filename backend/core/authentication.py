from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from django.http import JsonResponse
from rest_framework import status

class Custom_InvalidToken(InvalidToken):
    status_code=status.HTTP_200_OK

class Custom_JWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        details = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                details.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )
        
      
        raise Custom_InvalidToken(
            {
                "message": ("Given token not valid for any token type"),
                "details": details,
                "flag":'false',
                "status":'401'
            }
        )