from django.urls import path
from django.contrib.staticfiles.urls import static
from django.conf import settings
from . import views

app_name = 'music_player'

urlpatterns = [
    path('', views.player, name='player'),
]

# Addition for using uploaded media as static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
