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

class Writing(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    """Stores user id as foreign key."""
    title = models.TextField(max_length=200)
    """Title of the poem. Max length is 200."""
    body = MarkdownxField(null=True, blank=True)
    """The text body. Max length is based on underlying DB."""
    inspirations = models.TextField(null=True, blank=True)
    """Inspirations for the poem. Max length is based on underlying DB."""
    date_created = models.DateField()
    """Date the writing was created."""

class Writing_Author(models.Model):
    """
        Writing_Author model. Ties an author to a poem.
    """

    writing_id = models.ForeignKey(Writing, related_name='writings', on_delete=models.CASCADE)
    """Stores writing id as FK. related_name is writings""" 
    author_id = models.ForeignKey(Author, related_name='authors', on_delete=models.CASCADE)
    """Stores author id as FK. related_name is authors""" 

    #authors = Visual_Poetry_Author_QuerySet.as_manager()
    """The accessor for the Visual_Poetry_Author_QuerySet."""

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
