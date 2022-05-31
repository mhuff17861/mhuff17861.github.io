from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Views
def player(request):
    return render(request, 'portfolio_music_player/music_player.html')
