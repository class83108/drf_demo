from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

import logging


logger = logging.getLogger(__name__)


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        logger.debug(f"Headers: {request.headers}")

        header = self.get_header(request)
        if header is None:
            logger.debug("No Auth header found, checking cookies")
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
        else:
            logger.debug("Auth header found")
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            logger.debug("No token found")
            return None

        logger.debug("Token found, validating")
        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            logger.debug(f"Token validated, user: {user}")
            return user, validated_token
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            return None
