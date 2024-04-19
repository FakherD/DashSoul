from django.http import JsonResponse
from rest_framework.exceptions import APIException
import traceback
import logging
from rest_framework.exceptions import AuthenticationFailed
import jwt

class UserNotFoundException(APIException):
    status_code = 404
    default_detail = 'User not found'
    default_code = 'user_not_found'

class IncorrectPasswordException(APIException):
    status_code = 403
    default_detail = 'Incorrect Password'
    default_code = 'incorrect_password'

class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            if response.status_code == 500:
                # Log the error including a stack trace in production
                logger = logging.getLogger(__name__)
                logger.error(traceback.format_exc())
                return JsonResponse({'error': 'Internal Server Error'}, status=500)
            return response
        except Exception as e:
            return self.handle_exception(request, e)

    def handle_exception(self, exception):
        if isinstance(exception, AuthenticationFailed):
            return JsonResponse({
                'error': 'Authentication Failed',
                'details': str(exception)
            }, status=403)
        
        elif isinstance(exception, UserNotFoundException):
            return JsonResponse({
            'error': 'User not found',
            'details': str(exception)
        }, status=404)

        elif isinstance(exception, IncorrectPasswordException):
            return JsonResponse({
            'error': 'Incorrect Password',
            'details': str(exception)
        }, status=403)

        elif isinstance(exception, jwt.ExpiredSignatureError):
            return JsonResponse({
                'error': 'Token Expired',
                'details': 'Your session has expired. Please log in again.'
            }, status=401)  # 401 Unauthorized for expired tokens

        elif isinstance(exception, jwt.exceptions.PyJWTError):
            return JsonResponse({
                'error': 'Invalid Token',
                'details': 'The provided authentication token is invalid.'
            }, status=401)

        elif isinstance(exception, APIException):
            # Handle specific known API exceptions
            return JsonResponse({
                'error': 'API Error',
                'details': str(exception.detail)
            }, status=exception.status_code)

        else:
            # Log this error; it's unexpected
            logger = logging.getLogger(__name__)
            logger.error('Unhandled exception: %s\n%s', repr(exception), traceback.format_exc())
            return JsonResponse({
                'error': 'Internal Server Error',
                'details': 'An unexpected error occurred.'
            }, status=500)
