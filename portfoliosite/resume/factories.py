import factory
from factory.django import DjangoModelFactory
from .models import *
from datetime import datetime, timedelta

class UserFactory(DjangoModelFactory):
    class Meta:
        model = "users.User"

    username = 'test'
    password = 'test_pass'
    email = 'example@test.com'

PAGE_CHOICES = [x[0] for x in Page_Header.PAGE_CHOICES]
ALIGNMENT_CHOICES = [x[0] for x in Page_Header.ALIGNMENT_CHOICES]

class PageHeaderFactory(DjangoModelFactory):
    class Meta:
        model = 'resume.Page_Header'

    user_id = factory.SubFactory(UserFactory)
    name = factory.Iterator(PAGE_CHOICES)
    alignment = factory.Iterator(ALIGNMENT_CHOICES)
    image = factory.django.ImageField(color='blue')
    image_alt_text = "blue"
    title = factory.Faker('sentence', nb_words=3)
    body = factory.Faker('sentence', nb_words=100)

class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = 'resume.Project'

    user_id = factory.SubFactory(UserFactory)
    priority = factory.Faker('random_number', digits=1)
    title = factory.Faker('sentence', nb_words=4)
    image = factory.django.ImageField(color='blue')
    image_alt_text = "blue"
    short_description = factory.Faker('sentence', nb_words=40)
    long_description = factory.Faker('sentence', nb_words=100)
    start_date = factory.Faker('date_between',
        start_date=datetime.fromisoformat('2012-09-01'),
        end_date=datetime.fromisoformat('2022-04-01'))
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + timedelta(days=30)
        )
    url = factory.Faker('url')
    url_title = factory.Faker('sentence', nb_words=3)

class CVCategoryFactory(DjangoModelFactory):
    class Meta:
        model = 'resume.CV_Category'

    name = factory.Faker('sentence', nb_words=10)
    user_id = factory.SubFactory(UserFactory)
    priority = factory.Faker('random_number', digits=1)

class CVLineFactory(DjangoModelFactory):
    class Meta:
        model = 'resume.CV_Line'

    category = factory.SubFactory(CVCategoryFactory)
    user_id = factory.SubFactory(UserFactory)
    start_date = factory.Faker('date_between',
        start_date=datetime.fromisoformat('2012-09-01'),
        end_date=datetime.fromisoformat('2022-04-01'))
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + timedelta(days=30)
        )
    entry = factory.Faker('sentence', nb_words=25)

class CVSubLineFactory(DjangoModelFactory):
    class Meta:
        model = 'resume.CV_Sub_Line'

    cv_line = factory.SubFactory(CVLineFactory)
    entry = factory.Faker('sentence', nb_words=25)
