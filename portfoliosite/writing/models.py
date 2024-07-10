"""
This module holds the models for the writing app.
"""
from django.conf import settings
from django.db import models
from django.db.models import F
import logging

class Author(models.Model):
    """
        Author model. Stores writing authors.
    """

    name = models.TextField()
    """Stores name."""
    bio = models.TextField()
    """Stores author bio."""

class Visual_Poetry_QuerySet(models.QuerySet):
    """
    Poem_QuerySet. Provides functions for common queries on the VisualPoetry table.
    """

    pass

class Visual_Poetry(models.Model):
    """
    Visual_Poetry Model. Builds a model that allows the user to enter poetry with title,
    authorship, inspirations, and CSS for visual modifications.
    """
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    """Stores user id as foreign key."""
    title = models.TextField(max_length=100)
    """Title of the poem. Max length is 100."""
    image = models.ImageField(upload_to="visualpoetry")
    """Image that will be displayed with the poetry on the list page. Recommended aspect ratio is 7:5"""
    image_alt_text = models.TextField(max_length=50, default="picture description")
    """Alt text for the image, used for accessibility purposes. Max length is 50."""
    poem = models.TextField()
    """The poem in plain text. Max length is based on underlying DB."""
    # poem_template = models.TextField()
    """The template to call for building the visual poem. Max length is based on underlying DB."""
    # poem_css_file = models.TextField()
    """The css file to include. Max length is based on underlying DB."""
    inspirations = models.TextField()
    """Inspirations for the poem. Max length is based on underlying DB."""
    date_created = models.DateField()
    """Date the project ended."""

    #poems = Visual_Poetry_QuerySet.as_manager()
    """Accessor variable for the Visual_Poetry_QuerySet"""

class Visual_Poetry_Author_QuerySet(models.QuerySet):
    """
    Track_Number_QuerySet. Provides functions for common queries on the Track_Numbers table.
    """

    pass

class Visual_Poetry_Author(models.Model):
    """
        Visual_Poetry_Author model. Ties an author to a poem.
    """

    visual_poetry_id = models.ForeignKey(Visual_Poetry, related_name='authors', on_delete=models.CASCADE)
    """Stores song id as foreign key. related_name is track_nums""" 
    author_id = models.ForeignKey(Author, related_name='authors', on_delete=models.CASCADE)
    """Stores song id as foreign key. related_name is track_nums""" 

    authors = Visual_Poetry_Author_QuerySet.as_manager()
    """The accessor for the Visual_Poetry_Author_QuerySet."""

def __str__(self):
    return self.title
