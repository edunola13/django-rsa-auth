# Django RSA Auth
With this authentication and permission classes you can provide access to your endpoint throw RSA.

## Dependencies
 - django
 - rest_framework
 - cryptography

## Settings
 - PRIVATE_KEY: This is needed if you need to sign (encode).
 - ALLOWED_PUBLIC_KEYS: This is needed if you need to decode.
 - RSA_ALGORITHM: Algorithm to encode/decode.
 - JWT_AUTH_HEADER_PREFIX: Prefix for header "Authorization"

## How Work
In one point yo sign data and put in the header "Authorization".
In the other point yo receive the signed data in the header, try to decode throw the ALLOWED_PUBLIC_KEYS.
