from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit

@api_view(['GET'])
@ratelimit(key='user_or_ip', rate='10/m', block=False)
@ratelimit(key='ip', rate='5/m', block=True)
def login(request):
    return Response({
        'message': 'Login successful'
    })