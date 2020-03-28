import csv
import tempfile

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from books.models import Author


class ImportAuthorsTest(TestCase):
    """importauthors command Test Cases """

    def setUp(self):
        self.command = 'importauthors'
        self.authors = Author.objects.all()

    def _mock_csv_file(self, authors_list):
        """Receives a list of entries for the author csv file and returns the filename"""
        file = tempfile.NamedTemporaryFile(mode='w', delete=False)

        writer = csv.DictWriter(file, fieldnames=['name'])
        writer.writeheader()
        for author_name in authors_list:
            writer.writerow({'name': author_name})
        file.close()
        return file.name

    def test_import_authors(self):
        """Test successful import of unique author names"""
        author_list = ['J.K Rowling', 'J.D Salinger']
        file_path = self._mock_csv_file(author_list)
        call_command(self.command, file_path)

        self.assertEqual(len(self.authors), 2)
        self.assertIsNotNone(self.authors[0].id)
        self.assertIsNotNone(self.authors[0].name)

    def test_no_file(self):
        """Test import command without any file"""
        with self.assertRaises(CommandError) as context:
            call_command(self.command, '')
        self.assertIn('Oops, there was a problem processing your file - [Errno 2] ', str(context.exception))

    def test_empty_file(self):
        """Test import command with empty file"""
        author_list = []
        file_path = self._mock_csv_file(author_list)
        call_command(self.command, file_path)
        self.assertEqual(len(self.authors), 0)

    def test_import_repeated_authors(self):
        """Test import command with repeated author names"""
        author_list = ['J.K Rowling', 'J.K Rowling', 'J.D Salinger', 'J.D Salinger']
        file_path = self._mock_csv_file(author_list)
        call_command(self.command, file_path)

        self.assertEqual(len(self.authors.filter(name="J.K Rowling")), 1)
        self.assertEqual(len(self.authors), 2)
