from django.forms import ValidationError
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status, exceptions

class MyException(exceptions.APIException):
    status_code = 400
    default_detail = 'An error occurred'
    default_code = 'error'

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return Response({'detail': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if isinstance(exc, ValidationError):
        response.data['status_code'] = response.status_code

    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['detail'] = response.data.get('detail', str(exc))

    return response