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

    writings = Writing.writings.get_writings_by_date_created(10)

    context = {
        'writing_categories': [],
    }

    return render(request, 'writing/landing.html', context)

def writing(request, writing_id):
    """
        Returns the writing page for specific id
    """
    logger.debug(f'Retrieving writing id {writing_id}.')

    try:
        writing_item = Writing.writings.get_writing_by_id(writing_id)
    except Writing.DoesNotExist:
        Http404(f'No writing with id {writing_id} found.')

    context = {
        'writing_item': writing_item,
        'writing_id': writing_id,
    }

    return render(request, 'writing/writing.html', context)
