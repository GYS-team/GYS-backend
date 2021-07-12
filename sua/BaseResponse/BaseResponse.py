from rest_framework.response import Response
from rest_framework import status
from .ResponseConst import *
class BaseResponse(Response):
    def __init__(self, code=CODE_SUCCESS, message=MSG_SUCCESS, data={}, status=status.HTTP_200_OK,
                 content_type='application/json',exception=False):
        super(Response, self).__init__(None, status=status)
        self._code = code
        self._message = message
        self._data = data
        self.exception=exception
        self.data = {"code": code, "message": message, "data": data}
        
        self.content_type = content_type

