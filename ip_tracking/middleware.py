from .models import RequestLog, BlockedIP
from ipware import get_client_ip
from django.core.exceptions import PermissionDenied
from django.core.cache import cache


CACHE_TTL = 60 * 60 * 24
class LogRequestDetailsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        ip_address, _ = get_client_ip(request)
        path = request.path
        
        cache_key = f"ipaddress:{ip_address}"
        location = cache.get(cache_key)
        if location is None:
            location = getattr(request, 'geolocation', {}) or {}
            cache.set(cache_key, location, CACHE_TTL)

        log = RequestLog(
            ip_address=ip_address,
            path=path,
            country=location.get('country', 'Unknown'),
            city = location.get('city', 'Unknown')
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