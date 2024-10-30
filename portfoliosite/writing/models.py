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
    blurb = models.TextField(max_length=200)
    """Stores author bio."""

    def __str__(self):
        return self.name

class Writing_Category(models.Model):
    name = models.TextField()
    """Stores category name"""

class Writing_Project(models.Model):
    name = models.TextField()
    """Stores project name"""
    description = models.TextField()
    """Stores project description"""

class Writing_Topic_Tag(models.Model):
    name = models.TextField()
    """Stores tag name"""
    description = models.TextField()
    """Stores tag description"""

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
    category = models.ForeignKey(Writing_Category, on_delete=models.CASCADE)
    """The category of the writing"""
    project = models.ForeignKey(Writing_Project, null=True, on_delete=models.CASCADE)
    """The overall project of the writing belongs to"""
    tag = models.ManyToManyField(Writing_Topic_Tag, null=True)
    """The tag(s) that apply to the writing"""
    body = MarkdownxField(null=True, blank=True)
    """The text body. Max length is based on underlying DB."""
    inspirations = models.TextField(null=True, blank=True)
    """Inspirations for the poem. Max length is based on underlying DB."""
    date_created = models.DateField()
    """Date the writing was created."""
    published = models.BooleanField(null=True, blank=True, default=False)
    """Whether the writing should be published"""
    full_html_override = models.BooleanField(null=True, blank=True, default=False)
    """Whether the writing should be given a full html override"""
    writing_css_file = models.FileField(upload_to='writing/css', null=True)
    """The included CSS file"""

def __str__(self):
    return self.title
