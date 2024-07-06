import csv
from django.core.management.base import BaseCommand
from accounts.models import Account

class Command(BaseCommand):
    help = 'Ingest accounts from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Account.objects.create(
                    client_reference_no=row['client reference no'],
                    balance=row['balance'],
                    status=row['status'],
                    consumer_name=row['consumer name'],
                    consumer_address=row['consumer address'],
                    ssn=row['ssn']
                )
        self.stdout.write(self.style.SUCCESS('Successfully ingested accounts'))
