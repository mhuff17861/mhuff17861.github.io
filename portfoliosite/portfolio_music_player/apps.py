"""
    Auto-generated Django file for app configuration.
"""
import time
from django.apps import AppConfig
from . templatetags import version

class PortfolioMusicPlayerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio_music_player'

    def ready(self):
        version.version = int(round(time.time() * 1000))
