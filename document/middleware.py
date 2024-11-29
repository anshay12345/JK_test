import logging
import traceback
from django.http import JsonResponse
from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin


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



class LoggingMiddleware(MiddlewareMixin):
    """Middleware to log all requests and responses."""

    def process_request(self, request):
        """
        Logs the incoming request data.
        """
        try:
            content_type = request.content_type
            if "application/json" in content_type or "text" in content_type:
                # Decode and log only text-based body
                body = request.body.decode("utf-8") if request.body else "No Body"
            else:
                # Skip binary data
                body = "[Binary Data - Not Logged]"

            logger.info(f"Request Method: {request.method}")
            logger.info(f"Request Path: {request.path}")
            logger.info(f"Request Body: {body}")
        except Exception as e:
            logger.warning(f"Failed to log request body: {e}")
            

    def process_response(self, request, response):
        """ 
        Logs the outgoing response data.
        """
        try:
            # Log response status code
            logger.info(f"Response Status Code: {response.status_code}")

            # Check for the existence of response content
            if hasattr(response, "content"):
                # Handle multipart form data separately (skip logging large binary data)
                if request.content_type.startswith('multipart/form-data'):
                    body = 'Multipart form data; not logged due to potential large size or binary data'
                else:
                    # Safely decode the body with 'replace' for invalid characters
                    try:
                        body = request.body.decode('utf-8', errors='replace')
                    except Exception as e:
                        body = f"Error decoding body: {str(e)}"
                    logger.info(f"Response Body: {body}")

                # Check if response contains 'data' attribute (for DRF responses)
                if hasattr(response, 'data'):
                    response_data = response.data
                    if isinstance(response_data, dict):
                        for key, item in response_data.items():
                            # Log each key-value pair in the response data
                            logger.info(f"{key}: {item}")
                    else:
                        logger.info(f"Response data is not a dictionary: {response_data}")

            else:
                logger.error("Response has no content")

            logger.info("-" * 100)

        except Exception as e:
            logger.warning(f"Failed to log response content: {e}")

        return response
