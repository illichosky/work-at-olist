from rest_framework import serializers

from books.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'name')


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validate_data):
        authors = validate_data.pop('authors')
        instance = Book.objects.create(**validate_data)
        instance = self._append_author_objects(authors, instance, create=True)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.edition = validated_data.get('edition', instance.edition)
        instance.publication_year = validated_data.get('publication_year', instance.publication_year)

        authors = validated_data.get('authors', [])
        if authors:
            instance.authors.clear()
            instance = self._append_author_objects(authors, instance)

        instance.save()
        return instance

    @staticmethod
    def _append_author_objects(authors, instance, create=False):
        """Iterates over the authors list, find the Author object from that id and append to the Book obj"""
        for author in authors:
            try:
                author_object = Author.objects.get(id=author['id'])
                instance.authors.add(author_object)
            except Author.DoesNotExist:
                if create:
                    instance.delete()
                raise serializers.ValidationError({'detail': 'Author does not exists'})

        return instance
