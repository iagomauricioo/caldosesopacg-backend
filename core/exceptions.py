from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    """
    Custom exception handler for standardizing API error responses.
    """
    # First call REST framework's default exception handler
    response = exception_handler(exc, context)
    
    # If response is None, it means DRF can't handle the exception
    # so we need to handle it ourselves
    if response is None:
        if isinstance(exc, ObjectDoesNotExist):
            data = {
                'error': {
                    'type': 'not_found',
                    'message': str(exc),
                    'details': None
                }
            }
            response = Response(data, status=status.HTTP_404_NOT_FOUND)
            
        elif isinstance(exc, IntegrityError):
            data = {
                'error': {
                    'type': 'integrity_error',
                    'message': 'Database integrity error',
                    'details': str(exc)
                }
            }
            response = Response(data, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            data = {
                'error': {
                    'type': 'internal_error',
                    'message': 'An unexpected error occurred',
                    'details': str(exc)
                }
            }
            response = Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # If response exists, it means DRF handled the exception
    # but we want to standardize its format
    else:
        data = {
            'error': {
                'type': 'validation_error',
                'message': 'Invalid input data',
                'details': response.data
            }
        }
        response.data = data
    
    return response 