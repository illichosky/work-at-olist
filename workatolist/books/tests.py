import csv
import tempfile

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase

from books.factories import AuthorFactory, BookFactory
from books.models import Author, Book


class ImportAuthorsTest(TestCase):
    """importauthors command Test Cases """

    def setUp(self):
        self.command = 'importauthors'
        self.authors = Author.objects.all()

    @staticmethod
    def _mock_csv_file(authors_list):
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
        self.author = AuthorFactory(name='J.D Salinger')

    def test_list_authors(self):
        response = self.client.get(reverse('authors-list'))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertIn('next', response_data)
        results = response_data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 1)
        self.assertEqual(results[0]['name'], self.author.name)

    def test_get_author(self):
        response = self.client.get(reverse('authors-detail', kwargs={'name': self.author.name}))
        self.assertEqual(response.status_code, 200)

    def test_get_author_not_exist(self):
        response = self.client.get(reverse('authors-detail', kwargs={'name': 'Zé Ninguém'}))
        self.assertEqual(response.status_code, 404)


class BookViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = AuthorFactory(name='J.D Salinger')
        self.second_author = AuthorFactory(name='Hugo Pellissari')

        BookFactory(authors=[self.author], name='The Catcher in the Rye')
        BookFactory(authors=[self.author], name='The Catcher in the Rye', edition=2)

    def test_create_book(self):
        payload = {
            'name': 'The Catcher in the Rye',
            'authors': [{'id': self.author.id}],
            'edition': 1,
            'publication_year': 1951
        }
        response = self.client.post(reverse('books-list'), payload, format='json')
        self.assertEqual(response.status_code, 201)

        expected_response = {
            'id': 3,
            'authors': [{'id': self.author.id, 'name': self.author.name}],
            'name': 'The Catcher in the Rye',
            'edition': 1,
            'publication_year': 1951}
        self.assertEqual(response.json(), expected_response)

        books = Book.objects.all()
        self.assertEqual(len(books), 3)
        self.assertEqual(books[0].name, 'The Catcher in the Rye')

    def test_create_book_non_existent_author(self):
        payload = {
            'name': 'The Book That Should Never Be Written',
            'authors': [{'id': 123}],
            'edition': 1,
            'publication_year': 1951
        }
        response = self.client.post(reverse('books-list'), payload, format='json')
        self.assertEqual(response.json(), {'detail': 'Author does not exists'})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Book.objects.filter(name='The Book That Should Never Be Written').exists())

    def test_create_book_two_authors(self):
        payload = {
            'name': 'The Book that Never Existed',
            'authors': [{'id': self.author.id}, {'id': self.second_author.id}],
            'edition': 1,
            'publication_year': 1951
        }
        response = self.client.post(reverse('books-list'), payload, format='json')
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        book_authors = response_data['authors']
        self.assertEqual(len(book_authors), 2)
        self.assertTrue(Book.objects.all().exists())

    def test_create_book_incomplete_data(self):
        payload = {
            'name': 'The Book That Should Never Be Written',
            'authors': [self.author.id],
            'edition': 1,
        }
        response = self.client.post(reverse('books-list'), payload)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Book.objects.filter(name='The Book That Should Never Be Written').exists())

        payload = {
            'name': 'The Book That Should Never Be Written',
            'edition': 1,
        }
        response = self.client.post(reverse('books-list'), payload)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Book.objects.filter(name='The Book That Should Never Be Written').exists())

    def test_list_books(self):
        response = self.client.get(reverse('books-list'))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        expected_response = {
             'count': 2,
             'next': None,
             'previous': None,
             'results': [{'authors': [{'id': 13, 'name': 'J.D Salinger'}],
                          'edition': 1,
                          'id': 16,
                          'name': 'The Catcher in the Rye',
                          'publication_year': 2020},
                         {'authors': [{'id': 13, 'name': 'J.D Salinger'}],
                          'edition': 2,
                          'id': 17,
                          'name': 'The Catcher in the Rye',
                          'publication_year': 2020}]}

        self.assertEqual(response_data, expected_response)

    def test_filtered_list_books(self):
        books = Book.objects.all()
        self.assertEqual(len(books), 2)

        query = {'author': [self.author]}
        response = self.client.get(reverse('books-list'), data=query)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        results = response_data['results']
        self.assertEqual(len(results), 2)

        # do another call, but now filtering by edition
        query['edition'] = 2
        response = self.client.get(reverse('books-list'), data=query)
        response_data = response.json()
        results = response_data['results']
        self.assertEqual(len(results), 1)

        # try filtering with bad param, we should ignore it
        query['bad_param'] = 2
        response = self.client.get(reverse('books-list'), data=query)

        response_data = response.json()
        self.assertEqual(len(response_data['results']), 1)

    def test_update_book_edition(self):
        payload = {
            'name': 'The Book that Never Existed',
            'authors': [{'id': self.author.id}],
            'edition': 2,
            'publication_year': 1951
        }
        book_to_update = Book.objects.last()
        response = self.client.put(reverse('books-detail', kwargs={'pk': book_to_update.id}), payload, format='json')
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data['edition'], 2)

    def test_update_book_author(self):
        payload = {
            'name': 'The Book that Never Existed',
            'authors': [{'id': self.second_author.id}],
            'edition': 2,
            'publication_year': 1951
        }
        book_to_update = Book.objects.last()
        response = self.client.put(reverse('books-detail', kwargs={'pk': book_to_update.id}), payload, format='json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertEqual(len(response_data['authors']), 1)
        self.assertEqual(response_data['authors'][0]['name'], self.second_author.name)

    def test_update_book_no_author(self):
        payload = {
            'name': 'The Book that Never Existed',
            'edition': 2,
            'publication_year': 1951
        }
        book_to_update = Book.objects.last()
        response = self.client.put(reverse('books-detail', kwargs={'pk': book_to_update.id}), payload, format='json')
        self.assertEqual(response.status_code, 400)

    def test_partial_update_wrong_verb(self):
        payload = {
            'name': 'The Book that Never Existed',
            'authors': [{'id': self.second_author.id}],
            'publication_year': 1951
        }
        book_to_update = Book.objects.last()
        response = self.client.put(reverse('books-detail', kwargs={'pk': book_to_update.id}), payload, format='json')
        self.assertEqual(response.status_code, 400)

    def test_partial_update(self):
        payload = {
            'name': 'The Book that Never Existed',
            'authors': [{'id': self.second_author.id}],
            'publication_year': 1951
        }
        book_to_update = Book.objects.last()
        response = self.client.patch(reverse('books-detail', kwargs={'pk': book_to_update.id}), payload, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        initial_book_quantity = len(Book.objects.all())
        book_to_delete = Book.objects.last()
        response = self.client.delete(reverse('books-detail', kwargs={'pk': book_to_delete.id}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Book.objects.all()), initial_book_quantity-1)
