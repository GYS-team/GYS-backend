from rest_framework.views import exception_handler
from .ResponseConst import *
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    
    # Now add the HTTP status code to the response.
    if response is not None:
        if response.status_code>=500:
            return response
        response.data.clear()
        response.data= {}

        if response.status_code == 404:
            response.data['message'] = MSG_NOT_FOUND_ERROR
            response.data['code'] = CODE_NOT_FOUND_ERROR
            

        if response.status_code == 400:
            response.data['message'] = MSG_PARAMETER_ERROR
            response.data['code'] = CODE_PARAMETER_ERROR

        elif response.status_code == 401:
            response.data['message'] = exc.detail
            response.data['code'] = CODE_AUTH_ERROR

        elif response.status_code == 403:
            response.data['message'] = MSG_PERMISSIONS_ERROR
            response.data['code'] = CODE_PERMISSIONS_ERROR

        elif response.status_code == 405:
            response.data['message'] = MSG_METHOD_ERROR
            response.data['code'] = CODE_METHOD_ERROR
    return response
