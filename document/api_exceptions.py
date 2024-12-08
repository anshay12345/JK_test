from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    """
    A base class for creating custom exceptions in the application.
    It extends DRF's APIException to provide additional functionality for handling 
    error details and HTTP status codes.
    """
    detail=None
    status_code=None

    def __init__(self, detail, code=None):
        """
        Initializes the custom exception with a specific error message and status code.
        Args:
            detail (str): The error message to be returned to the client.
            code (int): The HTTP status code representing the type of error.

        This constructor:
        - Calls the parent `APIException`'s constructor using `super()`.
        - Sets the instance's `detail` and `status_code` attributes.
        """
        super().__init__(detail, code)
        self.detail=detail
        self.status_code=code

class FileNotUploadedException(BaseCustomException):
    """
    A specialized exception for handling cases where a file is not uploaded.
    Inherits from BaseCustomException and pre-defines the error message and status code.
    
    Attributes:
        detail (str): A human-readable message indicating the nature of the error.
    """
    def __init__(self):
        """
        Initializes the FileNotUploadedException with a fixed error message and status code.
        This constructor:
        - Sets a custom error message indicating that the file is not uploaded.
        - Calls the parent `BaseCustomException` constructor, passing the predefined
          error message and a 400 (Bad Request) status code.
        Args:
            None
        """
        detail="File not found. Please upload the file"
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)


class InvalidFileTypeException(BaseCustomException):
    """
    Exception raised for errors in the file type validation process.

    This exception is specifically used to indicate that a file uploaded
    is not of the expected PDF format. It inherits from BaseCustomException
    to provide a consistent exception handling mechanism across the application.

    Attributes:
        detail (str): A human-readable message indicating the nature of the error.
    """

    def __init__(self):
        """
        Initializes the InvalidFileTypeException with a predefined error message
        and HTTP status code.

        The error message is set to indicate that the uploaded file is not a PDF,
        and the HTTP status code is set to 400 (Bad Request) to reflect the client
        error in the request.

        Args:
            None
        """
        detail = "Uploaded file is not a PDF."
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)