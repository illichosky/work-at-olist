import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from books.models import Author


class Command(BaseCommand):
    help = 'Import author list from .csv file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Provides the authors csv file path')

    @transaction.atomic
    def handle(self, *args, **options):
        """Perform the operations to include authors into the DB. In case it fails, atomicity should rollback all the
        changes made up to that point"""
        try:
            file_path = options.get('file_path')
            data = csv.DictReader(open(file_path))
            for item in data:
                Author.objects.get_or_create(name=item['name'])
        except Exception as e:
            raise CommandError('Oops, there was a problem processing your file - {}'.format(e))
