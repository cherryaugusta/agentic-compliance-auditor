import uuid

from django.utils.deprecation import MiddlewareMixin


class CorrelationIdMiddleware(MiddlewareMixin):
    header_name = "HTTP_X_CORRELATION_ID"

    def process_request(self, request):
        request.correlation_id = request.META.get(self.header_name) or str(uuid.uuid4())

    def process_response(self, request, response):
        correlation_id = getattr(request, "correlation_id", None)
        if correlation_id:
            response["X-Correlation-ID"] = correlation_id
        return response
