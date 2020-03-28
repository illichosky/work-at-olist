import factory

from books.models import Author, Book


class AuthorFactory(factory.DjangoModelFactory):
    class Meta:
        model = Author


class BookFactory(factory.DjangoModelFactory):
    class Meta:
        model = Book

    name = 'Random book'
    edition = 1
    publication_year = 2020

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for author in extracted:
                self.authors.add(author)
