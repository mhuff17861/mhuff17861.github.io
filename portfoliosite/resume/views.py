from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from .models import Project, Page_Header, CV_Category

#  Helper functions!

def get_header(name):
    header = Page_Header.page_headers.get_header_for_page(name)

    if header:
        return header[0]

    return header

# Views
def index(request):
    cards = Project.projects.get_projects_by_priority(3).annotate(body=F('short_description'))

    context = {
        'header': get_header("Home"),
        'cards': cards,
    }

    return render(request, 'resume/home.html', context)

def projects(request):
    slides = Project.projects.get_projects_by_priority(3).annotate(body=F('long_description'))

    context = {
        'header': get_header("Projects"),
        'slides': slides,
    }

    return render(request, 'resume/projects.html', context)

def resume(request):
    cv_categories = CV_Category.cv_categories.get_categories_by_priority()
    for category in cv_categories:
        lines = []
        for line in category.cv_line_set.all():
            sub_lines = []
            for sub_line in line.cv_sub_line_set.all():
                sub_lines.append(sub_line)

            line.items = sub_lines
            lines.append(line)

        category.items = lines


    context = {
        'header': get_header("Resume"),
        'accordion_categories': cv_categories,
    }

    return render(request, 'resume/resume.html', context)
