from django.conf import settings
from django.db import models
from django.db.models import F

# ******** Models *****************

# Page_Header_QuerySet. Provides functions for common queries on the Page_Header table.
class Page_Header_QuerySet(models.QuerySet):
    # --- get_header_for_page(page_name) - Retrieves CV lines and their sub lines
    # for a specified category
    def get_header_for_page(self, page_name):
        return self.filter(name__iexact=page_name)

# Created for Page headers. Currently set to what portfolio app is for,
# home, resume, and projects.
class Page_Header(models.Model):
    class Meta:
        unique_together = (('name', 'user_id'),)

    user_id = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE
    )

    PAGE_CHOICES = (
        ('Home', 'Home page'),
        ('Projects', 'Projects page'),
        ('Resume', 'Resume page'),
    )
    name = models.TextField(choices=PAGE_CHOICES)

    ALIGNMENT_CHOICES = (
        ('L', 'Picture left aligned'),
        ('R', 'Picture right aligned'),
        ('C', 'Picture/text centered'),
    )
    alignment = models.TextField(choices=ALIGNMENT_CHOICES, default="L")

    image = models.ImageField(upload_to="page_headers")
    image_alt_text = models.TextField(max_length=50, default="picture description")
    title = models.TextField(max_length=25)
    body = models.TextField(max_length=700)

    page_headers = Page_Header_QuerySet.as_manager()

    def __str__(self):
        return str(self.user_id) + " - " + str(self.name)

# Project_QuerySet. Provides functions for common queries on the Projects table.
class Project_QuerySet(models.QuerySet):
    # --- get_projects_by_priority(num_projects) - Retrieves up to the designated number of projects from the
    # project model, with highest priority first.
    def get_projects_by_priority(self, num_projects):
        if self.count() <= num_projects:
            return self.order_by('priority')

        return self.order_by('priority')[:num_projects]

    # --- get_projects_by_start_date(num_projects): - Retrieves up to the
    # designated number of projects from the project model, with most recent start date first
    def get_projects_by_start_date(self, num_projects):
        if self.count() <= num_projects:
            return self.order_by('-start_date')

        return self.order_by('-start_date')[:num_projects]


# Project Model. Basic information and things that can be used for list displays
# (like the image and short/long descriptions). Can be extended later with
# related table allowing a "detail" construction.
class Project(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    priority = models.PositiveSmallIntegerField()
    title = models.TextField(max_length=50)
    image = models.ImageField(upload_to="projects")
    image_alt_text = models.TextField(max_length=50, default="picture description")
    short_description = models.TextField(max_length=120)
    long_description = models.TextField(max_length=600)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    url = models.TextField(max_length=100, blank=True, null=True)
    url_title = models.TextField(max_length=20, blank=True, null=True)

    projects = Project_QuerySet.as_manager()

    def __str__(self):
        return self.title

# CV_Category_QuerySet. Provides functions for common queries on the CV_Cateogorys table.
class CV_Category_QuerySet(models.QuerySet):
    # --- get_categories_by_priority() - Retrieves CV categories in order of priority
    def get_categories_by_priority(self):
        return self.order_by('priority')

    # --- get_categories_by_priority_with_lines() - Retrieves CV categories
    # in order of priority with associated cv_lines and sub_lines
    def get_categories_by_priority_with_lines(self):
        return self.order_by('priority').prefetch_related('cv_line_set')

# CV_Category Model. Defines broad categories, under which each line of a CV can be
# displayed.
class CV_Category(models.Model):
    class Meta:
        unique_together = (('name', 'user_id'),)

    name = models.TextField(max_length=100)
    user_id = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE
    )
    priority = models.PositiveSmallIntegerField()

    cv_categories = CV_Category_QuerySet.as_manager()

    def __str__(self):
        return self.name

# CV_Line_QuerySet. Provides functions for common queries on the CV_Lines table.
class CV_Line_QuerySet(models.QuerySet):
    # --- get_lines_full() - Retrieves CV lines and their sub lines
    def get_lines(self):
        return self

    # --- get_lines_full() - Retrieves CV lines and their sub lines
    def get_lines_by_start_date(self):
        return self.order_by('-start_date')

    # --- get_lines_full_for_category() - Retrieves CV lines and their sub lines
    # for a specified category
    def get_lines_for_category(self, category):
        return self.filter(category__exact=category)

        #CV_Line.cv_lines.get_lines_full_for_category(4)[0].cv_sub_line_set.all()[0]

# CV_Line Model. A single line entry meant to go under a CV category
class CV_Line(models.Model):
    user_id = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE
    )
    category = models.ForeignKey(CV_Category, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    entry = models.TextField(max_length=300)

    cv_lines = CV_Line_QuerySet.as_manager()

    def __str__(self):
        return str(self.category) + "-" + str(self.entry)
