from django.urls import path
from alx_backend_security.ip_tracking.views import login


urlpatterns = [
    path('login/', login)
]