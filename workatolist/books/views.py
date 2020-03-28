from rest_framework import viewsets

from books.models import Author
from books.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset to list and retrieve authors"""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'
