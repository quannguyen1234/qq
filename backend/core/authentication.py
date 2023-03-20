# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError

# class Custom_JWTAuthenticationn(JWTAuthentication):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     def get_validated_token(self, raw_token):
#         """
#         Validates an encoded JSON web token and returns a validated token
#         wrapper object.
#         """
#         messages = []
#         for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
#             try:
#                 return AuthToken(raw_token)
#             except TokenError as e:
#                 messages.append(
#                     {
#                         "token_class": AuthToken.__name__,
#                         "token_type": AuthToken.token_type,
#                         "message": e.args[0],
#                     }
#                 )

#         raise InvalidToken(
#             {
#                 "detail": _("Given token not valid for any token type"),
#                 "messages": messages,
#             }
#         )