"""
This module holds the models for the resume app.
"""
from django.conf import settings
from django.db import models
from django.db.models import F
import logging

logger = logging.getLogger(__name__)

# ******** Models *****************

class Page_Header_QuerySet(models.QuerySet):
    """
    Provides functions for common queries on the Page_Header table.
    """

    def get_header_for_page(self, page_name):
        """
        Retrieves CV lines and their sub lines
        for a specified category
        """
        logger.debug(f"Getting header for page {page_name}.")
        return self.filter(name__iexact=page_name)

class Page_Header(models.Model):
    """
    Created for Page headers. Currently only allows three page types:
    home, resume, and projects.
    """
    class Meta:
        unique_together = (('name', 'user_id'),)

    user_id = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE
    )
    """Stores user id as foreign key."""

    PAGE_CHOICES = (
        ('Home', 'Home page'),
        ('Projects', 'Projects page'),
        ('Resume', 'Resume page'),
    )
    """Choices for which page header is being edited"""
    name = models.TextField(choices=PAGE_CHOICES)
    """Stores the page name of the header. Limited to PAGE_CHOICES: Home, Projects, Resume."""

    ALIGNMENT_CHOICES = (
        ('L', 'Picture left aligned'),
        ('R', 'Picture right aligned'),
        ('C', 'Picture/text centered'),
    )
    """Choices for the alignment of the header image"""
    alignment = models.TextField(choices=ALIGNMENT_CHOICES, default="L")
    """Chooses where the image will be shown. Limited to ASSIGNMENT_CHOICES"""

    image = models.ImageField(upload_to="page_headers")
    """Image that will be displayed with the header. Recommended aspect ratio is 7:5."""
    image_alt_text = models.TextField(max_length=50, default="picture description")
    """Stores alt_text for the image, for accessibility purposes. Max length is 50."""
    title = models.TextField(max_length=25)
    """The heading that shows to the user when the header is assembled in html. Max length is 25."""
    body = models.TextField(max_length=700)
    """Body text that shows to the user when the header is assembled in html. Markdown enabled. Max length is 700."""
    page_headers = Page_Header_QuerySet.as_manager()
    """The accessor for the Page_Header_QuerySet."""

    def __str__(self):
        return str(self.user_id) + " - " + str(self.name)


class Project_QuerySet(models.QuerySet):
    """
    Project_QuerySet. Provides functions for common queries on the Projects table.
    """

    def get_projects_by_priority(self, num_projects):
        """
        get_projects_by_priority(num_projects) - Retrieves up to the designated number of projects from the
        project model, with highest priority first.
        """
        logger.debug(f"Getting {num_projects} projects by priority.")
        if self.count() <= num_projects:
            return self.order_by('priority')

        return self.order_by('priority')[:num_projects]

    def get_projects_by_start_date(self, num_projects):
        """
        get_projects_by_start_date(num_projects): - Retrieves up to the
        designated number of projects from the project model, with most recent start date first
        """
        logger.debug(f"Getting {num_projects} projects by start_date.")
        if self.count() <= num_projects:
            return self.order_by('-start_date')

        return self.order_by('-start_date')[:num_projects]

class Project(models.Model):
    """
    Project Model. Basic information and things that can be used for list displays
    (like the image and short/long descriptions). Can be extended later with
    related table allowing a "detail" construction.
    """
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    """Stores user id as foreign key."""
    priority = models.PositiveSmallIntegerField()
    """
        Priority decides the order in which projects will be displayed.
        Lower number means higher priority. Different projects can have the same priority.
    """
    title = models.TextField(max_length=50)
    """Title of the project. Max length is 50."""
    image = models.ImageField(upload_to="projects")
    """Image that will be displayed with the project. Recommended aspect ratio is 7:5"""
    image_alt_text = models.TextField(max_length=50, default="picture description")
    """Alt text for the image, used for accessibility purposes. Max length is 50."""
    short_description = models.TextField(max_length=120)
    """Short description, used when view has less space (example: card_layout). Max length is 120."""
    long_description = models.TextField(max_length=600)
    """Long description, used when view has more space (example: slide_layout). Max length is 600."""
    start_date = models.DateField()
    """Date the project started"""
    end_date = models.DateField(blank=True, null=True)
    """Date the project ended. Not required."""
    url = models.TextField(max_length=100, blank=True, null=True)
    """Url that will direct to the project. Max length is 100. Not required."""
    url_title = models.TextField(max_length=20, blank=True, null=True)
    """Title that will be shown instead of the full url. Max length is 20. Not required."""

    projects = Project_QuerySet.as_manager()
    """Accessor variable for the Project_QuerySet"""

    def __str__(self):
        return self.title

class CV_Category_QuerySet(models.QuerySet):
    """
    CV_Category_QuerySet. Provides functions for common queries on the CV_Cateogorys table.
    """

    def get_categories_by_priority(self):
        """
        get_categories_by_priority() - Retrieves CV categories in order of priority
        """
        logger.debug(f"Getting CV_Categories by priority.")
        return self.order_by('priority')

    def get_categories_by_priority_with_lines(self):
        """
        get_categories_by_priority_with_lines() - Retrieves CV categories
        in order of priority with associated cv_lines and sub_lines
        """
        logger.debug(f"Getting CV_Categories by priority with associated cv_lines.")
        return self.order_by('priority').prefetch_related('cv_line_set')

class CV_Category(models.Model):
    """
    CV_Category Model. Defines broad categories, under which each line of a CV can be
    displayed.
    """
    class Meta:
        unique_together = (('name', 'user_id'),)

    name = models.TextField(max_length=100)
    """Name of the category, used to organize cv_lines. Max length is 100."""
    user_id = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE
    )
    """Stores user id as foreign key."""
    priority = models.PositiveSmallIntegerField()
    """
        Priority decides the order in which cv_categories will be displayed.
        Lower number means higher priority. Different projects can have the same priority.
    """
    cv_categories = CV_Category_QuerySet.as_manager()
    """Accessor variable for the Project_QuerySet"""

    def __str__(self):
        return self.name


class CV_Line_QuerySet(models.QuerySet):
    """
    CV_Line_QuerySet. Provides functions for common queries on the CV_Lines table.
    """

    def get_lines(self):
        """
        get_lines() - Retrieves CV lines
        """
        logger.debug(f"Getting cv_lines")
        return self

    def get_lines_by_start_date(self):
        """
        get_lines_by_start_date() - Retrieves CV lines in order of start_date,
        most recent first
        """
        logger.debug(f"Getting cv_lines by start_date.")
        return self.order_by('-start_date')

    def get_lines_for_category(self, category):
        """
        get_lines_full_for_category(category) - Retrieves CV lines for a specified category
        """
        logger.debug(f"Getting cv_lines for category {category}")
        return self.filter(category__exact=category)

class CV_Line(models.Model):
    """
    CV_Line Model. A single line entry meant to go under a CV category
    """
    user_id = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE
    )
    """Stores user id as foreign key."""
    category = models.ForeignKey(CV_Category, on_delete=models.CASCADE)
    """Category that the CV_Line belongs to. Foreign key to CV_Cateogory.name"""
    start_date = models.DateField()
    """Date the cv entry started"""
    end_date = models.DateField(blank=True, null=True)
    """Date the cv entry ended"""
    entry = models.TextField(max_length=300)
    """Entry of the cv_line displayed on the site. Max length is 300"""

    cv_lines = CV_Line_QuerySet.as_manager()
    """Accessor variable for CV_Line_QuerySet."""

    def __str__(self):
        return str(self.category) + "-" + str(self.entry)
