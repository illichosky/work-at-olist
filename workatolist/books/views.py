from rest_framework import viewsets

from books.models import Author, Book
from books.serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset to list and retrieve authors"""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'


class BookViewSet(viewsets.ModelViewSet):
    """Viewset to list, retrive, create, update and delete books"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    valid_fields_filter_list = ['authors', 'edition', 'name', 'publication_year']

    def get_queryset(self):
        query_params = self.request.query_params
        if query_params:
            query = {}
            for valid_field in self.valid_fields_filter_list:
                if query_params.get(valid_field):
                    query[valid_field] = query_params.get(valid_field)
            return self.queryset.filter(**query)
        return self.queryset
