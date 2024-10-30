from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.db.models import F
from .models import Writing
import logging

logger = logging.getLogger(__name__)

#helpers 
def add_writing_context(writing, context):
    context['authors'] = writing.authors.all()
    context['inspirations'] = writing.inspirations

    return context

# Create your views here.
# Views
def writing_landing(request):
    """
        Returns the writing landing page
    """
    logger.debug(f'Retrieving writing view.')

    context = {
        'writing_categories': [
        ],
    }

    return render(request, 'writing/landing.html', context)

def writing(request):
    context = {

    }
    return render(request, 'writing/writing.html', context)