from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from .models import Project

# Create your views here.
def index(request):
    card_list = Project.projects.get_projects_by_priority(3).annotate(description=F('short_description'))
    context = {
        'card_list': card_list,
    }
    return render(request, 'resume/home.html', context)

def projects(request):
    return render(request, 'resume/projects.html')

def resume(request):
    return render(request, 'resume/resume.html')
