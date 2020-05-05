# -*- coding: utf-8 -*-
import logging
import jwt

from datetime import datetime

from django.conf import settings
from django.utils.encoding import smart_text

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header


def jwt_payload_handler(user=None):
    return {
        'orig_iat': datetime.utcnow().timestamp()
    }


def rsa_encode_handler(payload, key=None):
    key = key if key else settings.PRIVATE_KEY

    private_key = serialization.load_pem_private_key(
        key, None, default_backend()
    )

    return jwt.encode(
        payload,
        private_key,
        settings.RSA_ALGORITHM
    ).decode('utf-8')


def rsa_decode_handler(payload, key):
    return jwt.decode(
        payload,
        key,
        settings.RSA_ALGORITHM
    )


def get_jwt_value(request):
    auth = get_authorization_header(request).split()
    auth_header_prefix = settings.JWT_AUTH_HEADER_PREFIX.lower()
    if not auth or smart_text(auth[0].lower()) != auth_header_prefix:
        msg = 'Invalid Authorization header.'
        logging.error('[BaseAuthentication] {}'.format(msg))
        return False

    if len(auth) == 1:
        msg = 'Invalid Authorization header. No credentials provided.'
        logging.error('[BaseAuthentication] {}'.format(msg))
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = 'Invalid Authorization header. Credentials string should not contain spaces.'
        logging.error('[BaseAuthentication] {}'.format(msg))
        raise exceptions.AuthenticationFailed(msg)

    return auth[1]
