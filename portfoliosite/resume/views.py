from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from .models import Project, Page_Header, CV_Category
import logging

logger = logging.getLogger(__name__)

#  Helper functions!

def get_header(name):
    header = Page_Header.page_headers.get_header_for_page(name)

    if header:
        logger.debug(f'Returning header {header[0].name}')
        return header[0]

    logger.debug(f'no header found, returning None.')
    return header

# Views
def index(request):
    """
        Returns the home page, using the home template.
    """
    logger.debug(f'Retrieving index view.')
    cards = Project.projects.get_projects_by_priority(3).annotate(body=F('short_description'))

    if not cards:
        logger.warning(f'No projects retrieved for cards in index view')

    context = {
        'header': get_header("Home"),
        'cards': cards,
    }

    return render(request, 'resume/home.html', context)

def projects(request):
    """
        Returns the projects page, using the projects template.
    """
    logger.debug(f'Retrieving projects view.')
    slides = Project.projects.get_projects_by_priority(3).annotate(body=F('long_description'))

    if not slides:
        logger.warning(f'No projects retrieved for cards in projects view')

    context = {
        'header': get_header("Projects"),
        'slides': slides,
    }

    return render(request, 'resume/projects.html', context)

def resume(request):
    """
        Returns the resume page, using the resume template.
    """
    logger.debug(f'Retrieving resume view.')
    cv_categories = CV_Category.cv_categories.get_categories_by_priority_with_lines()

    if not cv_categories:
        logger.warning(f'No cv_categories retrieved for resume view.')

    """
    doing this because annotations (as far as I know) do not work on prefetched querysets
    and need to change for generalized accordion_layout
    """
    for category in cv_categories:
        lines = []
        for line in category.cv_line_set.order_by('-start_date'):
            lines.append(line)

        if not lines:
            logger.warning(f'No cv_lines retrieved for {category.name}.')
        category.items = lines


    context = {
        'header': get_header("Resume"),
        'accordion_categories': cv_categories,
    }

    return render(request, 'resume/resume.html', context)
