from django.shortcuts import render
from django.http import HttpResponse
from .models import Project

# Create your views here.
def index(request):
    context = {
        'card_list': Project.projects.get_projects_by_priority(3),
    }
    return render(request, 'resume/home.html', context)

def projects(request):
    return render(request, 'resume/projects.html')

def resume(request):
    return render(request, 'resume/resume.html')
