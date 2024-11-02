"""
This module holds the models for the writing app.
"""
from django.conf import settings
from django.db import models
from django.db.models import F
from markdownx.models import MarkdownxField
import logging

logger = logging.getLogger(__name__)

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

    def __str__(self):
        return self.name

class Writing_Project(models.Model):
    name = models.TextField()
    """Stores project name"""
    description = models.TextField()
    """Stores project description"""

    def __str__(self):
        return self.name

class Writing_Topic_Tag(models.Model):
    name = models.TextField()
    """Stores tag name"""
    description = models.TextField()
    """Stores tag description"""

    def __str__(self):
        return self.name

class Writing_QuerySet(models.QuerySet):
    """
    Writing_QuerySet. Provides functions for common queries on the Writings table.
    """

    def get_writings_by_category(self, category):
        """
        get_writings_by_category(category) - Retrieves all writing under a specified category
        """
        logger.debug(f"Getting writings in {category} category.")
        
        return self.filter(category__exact=category).filter(published=true).order_by('date_created')

    def get_writings_by_date_created(self, num_writings, page=0):
        """
        get_writings_by_date_created(num_writings, page=0): - Retrieves up to the
        designated number of writings from the project model, with most recent created date first
        """
        logger.debug(f"Getting {num_writings} writings by date_created.")

        if self.count() <= num_writings:
            return self.filter(published=True).order_by('-date_created')

        offset = page * num_writings

        return self.filter(published=True).order_by('-date_created')[offset:offset+num_writings]

    def get_writing_by_id(self, writing_id):
        """
        get_writing_by_id(writing_id) - Retrieves a writing by the given id
        """
        return self.filter(pk=writing_id).filter(published=True)

class Writing(models.Model):
    """Stores user id as foreign key."""
    title = models.TextField(max_length=200)
    """Title of the poem. Max length is 200."""
    authors = models.ManyToManyField(Author)
    """The author(s) of the writing"""
    category = models.ForeignKey(Writing_Category, on_delete=models.CASCADE)
    """The category of the writing"""
    project = models.ForeignKey(Writing_Project, null=True, blank=True, on_delete=models.CASCADE)
    """The overall project of the writing belongs to"""
    tags = models.ManyToManyField(Writing_Topic_Tag, null=True, blank=True)
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
    writing_css_file = models.FileField(upload_to='writing/css', null=True, blank=True)
    """The included CSS file"""

    writings = Writing_QuerySet.as_manager()
    """Accessor variable for the Writing_QuerySet"""

    def __str__(self):
        return self.title
