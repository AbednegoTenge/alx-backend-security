from django.db import models

# Create your models here.
class RequestLog(models.Model):
    ip_address = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=500)
    country = models.CharField(max_length=200, default="")
    city = models.CharField(max_length=200, default="")


class BlockedIP(models.Model):
    ip_address = models.CharField(max_length=200)


class SuspiciousIP(models.Model):
    ip_address = models.CharField(max_length=200)
    reason = models.TextField()