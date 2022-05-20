from django.conf import settings
from django.db import models

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

# Project Model. Basic information and things that can be used for list displays
# (like the image and short/long descriptions). Can be extended later with
# related table allowing a "detail" construction.
class Project (models.Model):
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
    end_date = models.DateField(blank=True)

# Project_Link Model. Allows user to have one or more links to project
# information/locations depending on the scope of the project. Priority
# used to establish link order/ decision in the case of cards.
class Project_Link(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    url = models.TextField(max_length=100)
    display_name = models.TextField(max_length=20)
    priority = models.PositiveSmallIntegerField()

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

# CV_Line Model. A single line entry meant to go under a CV category
class CV_Line(models.Model):
    user_id = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE
    )
    category = models.ForeignKey(CV_Category, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True)
    entry = models.TextField(max_length=300)

# CV_Sub_Line Model. Meant to make lines under CV lines, think 2nd level
# of a list in display.
class CV_Sub_Line(models.Model):
    class Meta:
        unique_together = (('cv_line_id', 'sub_entry'),)

    cv_line_id = models.ForeignKey(CV_Line, on_delete=models.CASCADE)
    sub_entry = models.TextField(max_length=300)
