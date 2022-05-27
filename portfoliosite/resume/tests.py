from django.test import TestCase, Client
from django.urls import reverse
from django.test.runner import DiscoverRunner
from datetime import date
from .models import Page_Header, Project, CV_Category, CV_Line, CV_Sub_Line
from .factories import *

#****************** Model Tests ****************

# Global settings for testing data creation.
NUM_PROJECTS = 5
NUM_CV_CATEGORIES = 10
NUM_CV_LINES = 10
NUM_CV_SUB_LINES = 3

# global functions for setUpTestData
def setup_data():
    user = UserFactory.create()
    PageHeaderFactory.create_batch(len(Page_Header.PAGE_CHOICES), user_id=user)
    ProjectFactory.create_batch(NUM_PROJECTS, user_id=user)
    categories = CVCategoryFactory.create_batch(NUM_CV_CATEGORIES, user_id=user)

    for i, category in enumerate(categories):
        cv_lines = CVLineFactory.create_batch(NUM_CV_LINES, category=category, user_id=user)
        for cv_line in cv_lines:
            CVSubLineFactory.create_batch(NUM_CV_SUB_LINES, cv_line=cv_line)



class PageHeaderTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        setup_data()

    def test_get_header_for_page(self):
        """
            Test the queryset get_header_for_page
        """
        PAGE_CHOICES = [x[0] for x in Page_Header.PAGE_CHOICES]
        for page in PAGE_CHOICES:
            test = Page_Header.page_headers.get_header_for_page(page)
            self.assertEqual(test[0].name, page)

class ProjectTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        setup_data()

    def test_get_projects_by_priority(self):
        """
            Test the queryset get_projects_by_priority
        """
        projects = Project.projects.get_projects_by_priority(NUM_PROJECTS)
        self.assertEqual(len(projects), NUM_PROJECTS)
        projects = Project.projects.get_projects_by_priority(NUM_PROJECTS-1)
        self.assertEqual(len(projects), NUM_PROJECTS-1)
        projects = Project.projects.get_projects_by_priority(NUM_PROJECTS+1)
        self.assertEqual(len(projects), NUM_PROJECTS)

        priority_test = 0
        for i, project in enumerate(projects):
            if i != (len(projects) - 1):
                self.assertGreaterEqual(project.priority, priority_test)
                priority_test = project.priority

    def test_get_projects_by_start_date(self):
        """
            Test the queryset get_projects_by_start_date
        """
        projects = Project.projects.get_projects_by_start_date(NUM_PROJECTS)
        self.assertEqual(len(projects), NUM_PROJECTS)
        projects = Project.projects.get_projects_by_start_date(NUM_PROJECTS-1)
        self.assertEqual(len(projects), NUM_PROJECTS-1)
        projects = Project.projects.get_projects_by_start_date(NUM_PROJECTS+1)
        self.assertEqual(len(projects), NUM_PROJECTS)

        date_test = date.fromisoformat('2030-01-01')
        for i, project in enumerate(projects):
            if i != (len(projects) - 1):
                self.assertLessEqual(project.start_date, date_test)
                date_test = project.start_date

class CVCategoryTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        setup_data()

    def test_get_categories_by_priority(self):
        """
            Test the queryset get_categories_by_priority
        """
        categories = CV_Category.cv_categories.get_categories_by_priority()
        self.assertTrue(categories)

        priority_test = 0
        for i, category in enumerate(categories):
            if i != (len(categories) - 1):
                self.assertGreaterEqual(category.priority, priority_test)
                priority_test = category.priority

class CV_Line_Tests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        setup_data()

    def test_get_lines_full(self):
        """
            Test the queryset get_lines_full
        """
        lines = CV_Line.cv_lines.get_lines_full()
        self.assertTrue(lines)

        for line in lines:
            self.assertTrue(line.cv_sub_line_set.all())

    def test_get_lines_full_by_start_date(self):
        """
            Test the queryset get_lines_full_by_start_date
        """
        lines = CV_Line.cv_lines.get_lines_full_by_start_date()

        date_test = date.fromisoformat('2030-01-01')
        for i, line in enumerate(lines):
            self.assertTrue(line.cv_sub_line_set.all())
            if i != (len(lines) - 1):
                self.assertLessEqual(line.start_date, date_test)
                date_test = line.start_date

    def test_get_full_for_category(self):
        """
            Test the queryset get_lines_full_for_category
        """
        categories = CV_Category.cv_categories.get_categories_by_priority()

        for category in categories:
            lines = CV_Line.cv_lines.get_lines_full_for_category(category.id)
            for line in lines:
                self.assertEqual(line.category.id, category.id)

class CV_Sub_Line_Tests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        setup_data()

    def test_get_sub_lines_for_line(self):
        """
            Test the queryset get_sub_lines_for_line
        """
        lines = CV_Line.cv_lines.get_lines_full()

        for line in lines:
            sub_lines = CV_Sub_Line.cv_sub_lines.get_sub_lines_for_line(line.id)
            self.assertTrue(sub_lines)
            for sub_line in sub_lines:
                self.assertEqual(sub_line.cv_line.id, line.id)

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
