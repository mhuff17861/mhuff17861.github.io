# Generated by Django 4.0.4 on 2022-06-02 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0010_rename_sub_entry_cv_sub_line_entry_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CV_Sub_Line',
        ),
    ]
