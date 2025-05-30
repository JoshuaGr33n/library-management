from django.conf import settings
from drf_yasg.utils import swagger_auto_schema

def hide_from_docs_yasg(dev_description, dev_response):
  
    def decorator(view_func):
        if not settings.DEBUG:
            return swagger_auto_schema(auto_schema=None)(view_func)
        return swagger_auto_schema(
            operation_description=dev_description,
            responses=dev_response
        )(view_func)
    return decorator





