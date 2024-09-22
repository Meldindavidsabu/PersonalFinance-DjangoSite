from django.core.management.base import BaseCommand
from expenses.views import send_weekly_summary

class Command(BaseCommand):
    help = 'Send weekly financial summaries to all users'

    def handle(self, *args, **options):
        send_weekly_summary()
        self.stdout.write(self.style.SUCCESS('Successfully sent weekly summaries.'))
