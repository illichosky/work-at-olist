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
        instance = self._append_author_objects(authors, instance)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('authors', instance.name)
        instance.edition = validated_data.get('edition', instance.edition)
        instance.publication_year = validated_data.get('publication_year', instance.publication_year)

        authors = validated_data.get('authors', [])
        instance = self._append_author_objects(authors, instance)

        instance.save()
        return instance

    @staticmethod
    def _append_author_objects(authors, instance):
        for author in authors:
            try:
                author_object = Author.objects.get(id=author['id'])
                instance.authors.add(author_object)
            except Author.DoesNotExist:
                raise serializers.ValidationError({'detail': 'Author does not exists'})

        return instance
