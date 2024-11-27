import logging
import traceback
from django.http import JsonResponse
from django.utils.timezone import now

# Setup logging to a file
logger = logging.getLogger('django')
file_handler = logging.FileHandler('logs/application.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ExceptionHandlingMiddleware:
    """
    Middleware for handling exceptions globally across all views.
    Catches unhandled exceptions and returns a JSON response with error details.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware with the next layer of the middleware or view to process requests.
        """
        self.get_response=get_response

    
    def __call__(self, request):
        """
        Process each request and catch any unhandled exceptions.
        Returns a JSON error response in case of an exception.
        """
        try:
            response = self.get_response(request)
        except Exception as e:
            logger.error("Unhandled Exception: %s", traceback.format_exc())
            response=JsonResponse(
                {"error": "Internal Server Error", "details": str(e)},
                status=500,
            )
        return response


class LoggingMiddleware:
    """
    Middleware for logging requests and responses to a file for auditing and debugging purposes.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware with the next layer of the middleware or view to process requests.
        """
        self.get_response=get_response

    
    def __call__(self, request):
        """
        Log details of the incoming request and outgoing response.
        """
        logger.info(
            f"Request - Method: {request.method}, Path: {request.path}, Time: {now()}, "
            f"Body: {request.body.decode('utf-8') if request.body else 'No Body'}"
        )

        response=self.get_response(request)
        logger.info(
            f"Response - Status: {response.status_code}, Content: {response.content.decode('utf-8')}"
        )
        return response