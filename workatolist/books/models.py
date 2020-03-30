from django.db import models


class Author(models.Model):
    """Model representing book authors"""
    name = models.CharField(max_length=200, help_text="Author name")


class Book(models.Model):
    """Model representing books"""
    name = models.CharField(max_length=200, help_text="Book name")
    edition = models.PositiveSmallIntegerField(help_text="Book edition")
    publication_year = models.PositiveSmallIntegerField(help_text="Year the book was published")
    authors = models.ManyToManyField(Author, help_text="Authors of the book")
