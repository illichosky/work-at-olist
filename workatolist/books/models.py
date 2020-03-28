from django.db import models


class Author(models.Model):
    """Model representing book authors"""
    name = models.CharField(max_length=200)


class Book(models.Model):
    """Model representing books"""
    name = models.CharField(max_length=200)
    edition = models.PositiveSmallIntegerField()
    publication_year = models.PositiveSmallIntegerField()
    authors = models.ManyToManyField(Author)
