from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from apps.User.models import BaseUser
from django.contrib.auth.models import AnonymousUser
import json,os
from asgiref.sync import sync_to_async

class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """
 
    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner
        self.User = BaseUser()

    
    async def __call__(self, scope,receive, send):
 
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()
        user=AnonymousUser()
        # Get the token
        headers=scope["headers"]
    
        
        result = {}
        for item in headers:
            result[item[0].decode()] = item[1].decode()
        # Try to authenticate the user
        # token=result['access']
        token=scope['path'].split('/')[-1]
        print("------",token,"-----")
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:        
            pass
        else:
            #  Then token is valid, decode it
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user=  await sync_to_async(BaseUser.objects.get)(id=decoded_data["user_id"])
                
        scope['user'] = user
        return await self.inner(scope, receive, send)