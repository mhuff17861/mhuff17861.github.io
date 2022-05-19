from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'resume/home.html')

def projects(request):
    return render(request, 'resume/projects.html')

def resume(request):
    return render(request, 'resume/resume.html')
