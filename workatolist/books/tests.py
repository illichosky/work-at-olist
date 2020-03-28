import csv
import tempfile

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase

from books.factories import AuthorFactory
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


class AuthorViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.author_name = 'J.D Salinger'
        self.author = AuthorFactory(name=self.author_name)

    def test_list_authors(self):
        response = self.client.get(reverse('authors-list'))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertIn('next', response_data)
        results = response_data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 1)
        self.assertEqual(results[0]['name'], self.author_name)

    def test_get_author(self):
        response = self.client.get(reverse('authors-detail', kwargs={'name': self.author_name}))
        self.assertEqual(response.status_code, 200)

    def test_get_author_not_exist(self):
        response = self.client.get(reverse('authors-detail', kwargs={'name': 'Zé Ninguém'}))
        self.assertEqual(response.status_code, 404)
