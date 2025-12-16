from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def test_logging_view(request):
    # Zichtbare prints zodat we weten dat de view bereikt wordt
    print(">>> VIEW PRINT: test_logging_view reached")
    logger.debug(">>> DEBUG from test_logging_view")
    logger.info(">>> INFO from test_logging_view")
    logger.error(">>> ERROR from test_logging_view")
    return HttpResponse("logging test done")

