"""
    This file renders the proper template for each view in the portfolio_music_player app.
"""
from django.shortcuts import render
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

# Create your views here.

# Views
def player(request):
    """Returns the music player with the music_player template."""
    logger.debug(f'Retrieving player view.')
    return render(request, 'portfolio_music_player/music_player.html')
