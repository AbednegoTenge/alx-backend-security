from .models import RequestLog, BlockedIP
from ipware import get_client_ip
from django.core.exceptions import PermissionDenied

class LogRequestDetailsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address, _ = get_client_ip(request)
        path = request.path

        log = RequestLog(
            ip_address=ip_address,
            path=path
        )
        log.save()

        response = self.get_response(request)
        return response
    

class BlacklistMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        ip_address, _ = get_client_ip(request)
        
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            raise PermissionDenied("Your IP has been blocked")

        response = self.get_response(request)
        return response