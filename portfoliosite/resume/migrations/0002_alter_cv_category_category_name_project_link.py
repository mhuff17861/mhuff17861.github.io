# Generated by Django 4.0.4 on 2022-05-20 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cv_category',
            name='category_name',
            field=models.TextField(max_length=100),
        ),
        migrations.CreateModel(
            name='Project_Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(max_length=100)),
                ('display_name', models.TextField(max_length=20)),
                ('priority', models.PositiveSmallIntegerField()),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.project')),
            ],
        ),
    ]
