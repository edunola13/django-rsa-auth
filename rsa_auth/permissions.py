from django.conf import settings
from rest_framework import permissions


class RSAPermission(permissions.BasePermission):
    """
    Allows only to RSA decoded payloads.
    """

    def has_permission(self, request, view):
        return request._auth
