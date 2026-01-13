from django.core.management.base import BaseCommand, CommandError
from alx_backend_security.ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help="""A management command to block IP address"""

    def add_arguments(self, parser):
        parser.add_argument(
            'ip_address',
            type=str,
            help="IP address to block"
        )

    
    def handle(self, *args, **options):
        ip_address = options['ip_address']

        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            raise CommandError(f"IP address {ip_address} is already blocked")

        BlockedIP.objects.create(ip_address=ip_address)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully blocked IP address: {ip_address}")
        )

        