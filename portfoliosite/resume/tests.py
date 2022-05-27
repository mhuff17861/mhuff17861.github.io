from django.test import TestCase, Client
from django.urls import reverse
from .models import Page_Header, Project, CV_Category, CV_Line, CV_Sub_Line
from .factories import *

#****************** Model Tests ****************

class PageHeaderTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        user = UserFactory.create()
        PageHeaderFactory.create_batch(3, user_id=user)
        ProjectFactory.create_batch(3, user_id=user)
        categories = CVCategoryFactory.create_batch(10, user_id=user)

        for i, category in enumerate(categories):
            cv_lines = CVLineFactory.create_batch(10, category=category, user_id=user)
            if (i % 3) == 0:
                for cv_line in cv_lines:
                    CVSubLineFactory.create_batch(3, cv_line_id=cv_line)

    def test_get_header_for_page(self):
        """
            Test the queryset get_header_for_page
        """
        PAGE_CHOICES = [x[0] for x in Page_Header.PAGE_CHOICES]
        for page in PAGE_CHOICES:
            test = Page_Header.page_headers.get_header_for_page(page)
            self.assertEqual(test[0].name, page)

#********* View Tests **********

class IndexViewTests(TestCase):

    def test_index_no_data_response(self):
        """
            Test the index url for error free page return
        """
        client = Client()
        response = self.client.get(reverse('resume:index'))
        self.assertEqual(response.status_code, 200)

class ProjectsViewTests(TestCase):

    def test_projects_no_data_response(self):
        """
            Test the index url for error free page return
        """
        client = Client()
        response = self.client.get(reverse('resume:projects'))
        self.assertEqual(response.status_code, 200)


class ResumeViewTests(TestCase):

    def test_resume_no_data_response(self):
        """
            Test the index url for error free page return
        """
        client = Client()
        response = self.client.get(reverse('resume:resume'))
        self.assertEqual(response.status_code, 200)
