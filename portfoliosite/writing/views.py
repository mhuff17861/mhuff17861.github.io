from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.db.models import F
from django.forms.models import model_to_dict
from .models import Writing
import logging

logger = logging.getLogger(__name__)


# Create your views here.
# Views
def writing_landing(request):
    """
        Returns the writing landing page
    """
    logger.debug(f'Retrieving writing view.')

    writings = Writing.writings.get_writings_by_date_created(10)

    context = {
        'writings': [],
        'writing_url_slug': '/writing/piece/',
    }

    for writing in writings:
        item = writing
        item = add_writing_context(writing, model_to_dict(item))
        context['writings'].append(item)

    return render(request, 'writing/landing.html', context)

def writing_category(request, category_id=None):
    #with no category, try a group by or something?
    pass

def writing_project(request, project_id=None):
    pass

def writing_topic_tag(request, topic_tag_id=None):
    pass

def writing(request, writing_id):
    """
        Returns the writing page for specific id
    """
    logger.debug(f'Retrieving writing id {writing_id}.')

    writing = Writing.writings.get_writing_by_id(writing_id)
    writing_item = writing.first()

    if not writing_item:
        raise Http404(f'No writing with id {writing_id} found.')

    writing_item = add_writing_context(writing_item, model_to_dict(writing_item))

    context = {
        'writing_item': writing_item,
        'writing_id': writing_id,
    }

    return render(request, 'writing/writing.html', context)

"""*********************** Helpers *******************"""

def group_writing_by_field(writing, field="category"):
    categorized_writing = {}

    for piece in writing:
        if piece[field] not in categorized_writing:
            categorized_writing[piece[field]] = []

        categorized_writing[piece[field]].append(piece)

    return categorized_writing

def add_writing_context(writing, context):
    context['authors'] = writing.authors.all()
    context['project'] = writing.project
    context['category'] = writing.category
    context['tags'] = writing.tags.all()
    context['inspirations'] = writing.inspirations

    return context
