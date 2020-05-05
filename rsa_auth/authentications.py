import jwt
import logging

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication as DRFBaseAuthentication
)

from .jwt import get_jwt_value, rsa_decode_handler

User = get_user_model()


class RSAAuthentication(DRFBaseAuthentication):

    def authenticate(self, request):
        if settings.TESTING:
            return 'localhost', 'fakepayload'

        jwt_value = get_jwt_value(request)

        if not jwt_value:
            msg = 'Missing RSA key on Authorization Header'
            logging.error('[RSAAuthentication] {}'.format(msg))
            raise exceptions.AuthenticationFailed(msg)

        payload = None
        msg = 'Error decoding signature.'

        for allowed_key in settings.ALLOWED_PUBLIC_KEYS:
            try:
                payload = rsa_decode_handler(jwt_value, allowed_key)
                break
            except jwt.ExpiredSignature:
                msg = 'Signature has expired.'
                logging.error('[RSAAuthentication] {}'.format(msg))
                raise exceptions.AuthenticationFailed(msg)
            except jwt.DecodeError:
                # Try another allowed_key
                pass

        if not payload:
            logging.error('[RSAAuthentication] {}'.format(msg))
            raise exceptions.AuthenticationFailed(msg)

        return '', payload


class RSAAuthenticationUser(RSAAuthentication):

    def authenticate(self, request):
        # Check the RSA and return the payload
        app, payload = super(RSAAuthenticationUser, self).authenticate(request)

        if payload is None or 'user_id' not in payload:
            return None

        try:
            user = User.objects.get(id=payload.get('user_id'))
        except User.DoesNotExist:
            return None

        return (user, None)
