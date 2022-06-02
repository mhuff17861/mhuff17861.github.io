from django.shortcuts import render
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

# Create your views here.

# Views
def player(request):
    logger.debug(f'Retrieving player view.')
    return render(request, 'portfolio_music_player/music_player.html')
