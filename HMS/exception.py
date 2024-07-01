from django.http import JsonResponse
from rest_framework.views import exception_handler as drf_exception_handler

class CustomException(Exception):
    detail = None
    status_code = None

    
    def __init__(self, status_code,message):
        CustomException.status_code = status_code
        CustomException.detail = message
    

def customExceptionHandler(exception,context):

    response = drf_exception_handler(exc=exception,context=context)

    if response is not None:
        if isinstance(exception,CustomException):
         response.data['status_code'] = response.status_code
         response.data['message'] = response.data['detail']
         del response['message'] #changing the detail keu with message key by deleting detail key
         return response
        