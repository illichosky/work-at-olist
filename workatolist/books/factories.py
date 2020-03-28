import factory

from books.models import Author


class AuthorFactory(factory.DjangoModelFactory):
    class Meta:
        model = Author
