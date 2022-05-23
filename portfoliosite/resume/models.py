from django.conf import settings
from django.db import models
from django.db.models import F

# ******** Models *****************

# Created for Page headers. Currently set to what portfolio app is for,
# home, resume, and projects.
class Page_Header(models.Model):
    class Meta:
        unique_together = (('name', 'user_id'),)

    PAGE_CHOICES = (
        ('H', 'Home'),
        ('P', 'Projects'),
        ('R', 'Resume'),
    )
    name = models.TextField(choices=PAGE_CHOICES)
    user_id = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="page_headers")
    title = models.TextField(max_length=25)
    body = models.TextField(max_length=25)

# ProjectQuerySet. Provides functions for common queries on the Projects table.
# NOTE: NEEDS TO GET PROJECT LINK SOMEHOW.
class ProjectQuerySet(models.QuerySet):
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
            return self.order_by('start_date')

        return self.order_by('start_date')[:num_projects]


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
    short_description = models.TextField(max_length=120)
    long_description = models.TextField(max_length=600)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    url = models.TextField(max_length=100, blank=True, null=True)
    url_title = models.TextField(max_length=20, blank=True, null=True)

    projects = ProjectQuerySet.as_manager()

    def __str__(self):
        return self.title

# CV_Category Model. Defines broad categories, under which each line of a CV can be
# displayed.
class CV_Category(models.Model):
    class Meta:
        unique_together = (('category_name', 'user_id'),)

    category_name = models.TextField(max_length=100)
    user_id = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE
    )
    priority = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.category_name

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

    def __str__(self):
        return "-".join([self.category, self.entry])

# CV_Sub_Line Model. Meant to make lines under CV lines, think 2nd level
# of a list in display.
class CV_Sub_Line(models.Model):
    class Meta:
        unique_together = (('cv_line_id', 'sub_entry'),)

    cv_line_id = models.ForeignKey(CV_Line, on_delete=models.CASCADE)
    sub_entry = models.TextField(max_length=300)

    def __str__(self):
        return self.sub_entry
