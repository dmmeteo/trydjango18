from django.core.management.base import BaseCommand
from cron import cron_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        cron_task()
