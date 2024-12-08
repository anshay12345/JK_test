from rest_framework.views import exception_handler
from datetime import datetime


def custom_exception_handler(exc, context):
    """
    Custom exception handler that adds additional information to the response.

    Args:
        exc: The exception instance.
        context: The context in which the exception occurred.

    Returns:
        A Response object with additional fields: 'message', 'time', and 'status_code'.
    """
    
    # Call REST framework's default exception handler first, to get the standard error response.
    response=exception_handler(exc, context)

    if response is not None:
        response.data['message'] = response.data['detail']
        response.data['time'] = datetime.now()
        response.data['status_code'] = response.status_code
        del response.data['detail']
    return response