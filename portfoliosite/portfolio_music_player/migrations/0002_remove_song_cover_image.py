# Generated by Django 4.0.4 on 2022-07-14 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_music_player', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='cover_image',
        ),
    ]