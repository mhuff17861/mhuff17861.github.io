from django.test import TestCase, Client
from django.urls import reverse

#********* View Tests **********

class IndexViewTests(TestCase):

    def test_index_response(self):
        """
            Test the index url for error free page return
        """
        client = Client()
        response = self.client.get(reverse('resume:index'))
        self.assertEqual(response.status_code, 200)

class ProjectsViewTests(TestCase):

    def test_projects_response(self):
        """
            Test the index url for error free page return
        """
        client = Client()
        response = self.client.get(reverse('resume:projects'))
        self.assertEqual(response.status_code, 200)


class ResumeViewTests(TestCase):

    def test_resume_response(self):
        """
            Test the index url for error free page return
        """
        client = Client()
        response = self.client.get(reverse('resume:resume'))
        self.assertEqual(response.status_code, 200)
