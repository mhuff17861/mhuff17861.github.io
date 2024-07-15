from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.db.models import F
from .models import Visual_Poetry, Article
import logging

logger = logging.getLogger(__name__)

#helpers 
def add_writing_context(writing, context):
    context['authors'] = writing.authors.all()
    context['inspirations'] = writing.inspirations

    return context

# Create your views here.
# Views
def writing(request):
    """
        Returns the writing landing page
    """
    logger.debug(f'Retrieving writing view.')

    articles = Article.objects.filter(published=True)
    poems = Visual_Poetry.objects.filter(published=True)

    context = {
        'writing_categories': [
            {
                'title': 'Articles',
                'items': articles,
                'slug': 'article/',
            },
            {
                'title': 'Visual Poems',
                'items': poems,
                'slug': 'poem/',
            },
        ],
    }

    return render(request, 'writing/landing.html', context)

def article(request, article_id):
    """
        Returns an article
    """
    logger.debug(f'Retrieving article view')

    try:
        article = Article.objects.get(pk=article_id, published=True)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    context = {
        'article': article,
        'writing_type': 'article',
    }

    context = add_writing_context(article, context)

    return render(request, 'writing/article.html', context)

def visual_poetry(request, poem_id):
    """
        Returns a visual poetry page
    """
    logger.debug(f'Retrieving visual poetry view')

    try:
        poem = Visual_Poetry.objects.get(pk=poem_id, published=True)
    except Visual_Poetry.DoesNotExist:
        raise Http404("Poem does not exist")

    context = {
        'poem': poem,
        'writing_type': 'poem',
    }

    context = add_writing_context(poem, context)

    return render(request, 'writing/visual_poetry.html', context)