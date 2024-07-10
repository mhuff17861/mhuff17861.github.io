from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
#from .models import Project, Page_Header, CV_Category
import logging

logger = logging.getLogger(__name__)

# Create your views here.
# Views
def writing(request):
    """
        Returns the writing landing page
    """
    logger.debug(f'Retrieving writing view.')

    context = {
    }

    return render(request, 'writing/landing.html', context)