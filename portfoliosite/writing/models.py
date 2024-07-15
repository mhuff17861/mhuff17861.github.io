"""
This module holds the models for the writing app.
"""
from django.conf import settings
from django.db import models
from django.db.models import F
from markdownx.models import MarkdownxField
import logging

class Author(models.Model):
    """
        Author model. Stores writing authors.
    """

    name = models.TextField()
    """Stores name."""
    bio = MarkdownxField(null=True, blank=True)
    """Stores author bio."""

    def __str__(self):
        return self.name

class Writing(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    """Stores user id as foreign key."""
    title = models.TextField(max_length=200)
    """Title of the poem. Max length is 200."""
    authors = models.ManyToManyField(Author)
    """The author(s) of the writing"""
    body = MarkdownxField(null=True, blank=True)
    """The text body. Max length is based on underlying DB."""
    inspirations = models.TextField(null=True, blank=True)
    """Inspirations for the poem. Max length is based on underlying DB."""
    date_created = models.DateField()
    """Date the writing was created."""
    published = models.BooleanField(null=True, blank=True)
    """Whether the writing should be published"""

    class Meta:
        abstract = True

class Article_Category(models.Model):
    """
        Article Categories to place articles into.
    """

    category = models.TextField(max_length=100)
    """Name of the category, used to organize cv_lines. Max length is 100."""

    def __str__(self):
        return self.category

class Article(Writing):
    """
        Article model, used to create various writings in various categories.
    """
    categories = models.ManyToManyField(Article_Category)

    def __str__(self):
        return str(self.title)

class Visual_Poetry_QuerySet(models.QuerySet):
    """
    Poem_QuerySet. Provides functions for common queries on the VisualPoetry table.
    """

    pass

class Visual_Poetry(Writing):
    """
    Visual_Poetry Model. Builds a model that allows the user to enter poetry with title,
    authorship, inspirations, and CSS for visual modifications.
    """
    
    poem_css_file = models.FileField(upload_to='visual_poetry/poem_css', null=True)
    """The css file to include. WARNING: Unsafe without filtering, only doing because I'm the only user. Max length is based on underlying DB."""

    #poems = Visual_Poetry_QuerySet.as_manager()
    """Accessor variable for the Visual_Poetry_QuerySet"""


def __str__(self):
    return self.title
