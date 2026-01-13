from celery import shared_task
from alx_backend_security.ip_tracking.models import RequestLog, SuspiciousIP
from django.utils import timezone
from datetime import timedelta


SENSITIVE_PATHS = ['/admin', '/login']

@shared_task
def flag_suspicious_ips(request, *args, **kwargs):
    """
    Flags IPs that:
    1. Made > 100 requests in the past hour
    2. Accessed sensitive paths
    """
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)

    logs_last_hour = RequestLog.objects.filter(timestamp__gte=one_hour_ago)
    ip_counts = {}

    for log in logs_last_hour:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(ip_address=ip)

    # 2️⃣ IPs accessing sensitive paths
    sensitive_logs = RequestLog.objects.filter(path__in=SENSITIVE_PATHS, timestamp__gte=one_hour_ago)
    for log in sensitive_logs:
        SuspiciousIP.objects.get_or_create(ip_address=log.ip_address)

    return f"Flagged {len(ip_counts)} IPs in the last hour"

