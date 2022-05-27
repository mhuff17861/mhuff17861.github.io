from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from .models import Project, Page_Header

#  Helper functions!

def get_header(name):
    header = Page_Header.page_headers.get_header_for_page(name)

    if header:
        return header[0]

    return header

# Views
def index(request):
    card_list = Project.projects.get_projects_by_priority(3).annotate(description=F('short_description'))

    context = {
        'header': get_header("Home"),
        'card_list': card_list,
    }

    return render(request, 'resume/home.html', context)

def projects(request):
    context = {
        'header': get_header("Projects"),
    }

    return render(request, 'resume/projects.html', context)

def resume(request):
    context = {
        'header': get_header("Resume"),
    }

    return render(request, 'resume/resume.html', context)
