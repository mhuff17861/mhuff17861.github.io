from django.test import TestCase, Client
from django.urls import reverse
from django.test.runner import DiscoverRunner
from datetime import date
from .models import Page_Header, Project, CV_Category, CV_Line
from .factories import *

# ****************Helper Functions/Variables***********
# Global settings for testing data creation.
NUM_PROJECTS = 5
NUM_CV_CATEGORIES = 10
NUM_CV_LINES = 10

# global functions for setUpTestData
def setup_data():
    user = UserFactory.create()
    PageHeaderFactory.create_batch(len(Page_Header.PAGE_CHOICES), user_id=user)
    ProjectFactory.create_batch(NUM_PROJECTS, user_id=user)
    categories = CVCategoryFactory.create_batch(NUM_CV_CATEGORIES, user_id=user)

    for i, category in enumerate(categories):
        cv_lines = CVLineFactory.create_batch(NUM_CV_LINES, category=category, user_id=user)

#****************** Model Tests ****************

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
        msg_amount = "Project QuerySet get_projects_by_priority did not return the correct amount of projects -- "
        projects = Project.projects.get_projects_by_priority(NUM_PROJECTS)
        self.assertEqual(len(projects), NUM_PROJECTS, msg=msg_amount + "Max Num Test")
        projects = Project.projects.get_projects_by_priority(NUM_PROJECTS-1)
        self.assertEqual(len(projects), NUM_PROJECTS-1, msg=msg_amount + "Less than Max Num Test")
        projects = Project.projects.get_projects_by_priority(NUM_PROJECTS+1)
        self.assertEqual(len(projects), NUM_PROJECTS, msg=msg_amount + "More than Max Num Test")

        priority_test = 0
        for i, project in enumerate(projects):
            if i != (len(projects) - 1):
                self.assertGreaterEqual(project.priority, priority_test,
                    msg="Project Queryset get_projects_by_priority returned projects in the wrong order of priority. Expect lowest number (highest priority) first")
                priority_test = project.priority

    def test_get_projects_by_start_date(self):
        """
            Test the queryset get_projects_by_start_date
        """
        msg_amount = "Project QuerySet get_projects_by_start_date did not return the correct amount of projects -- "
        projects = Project.projects.get_projects_by_start_date(NUM_PROJECTS)
        self.assertEqual(len(projects), NUM_PROJECTS, msg=msg_amount  + "Max Num Test")
        projects = Project.projects.get_projects_by_start_date(NUM_PROJECTS-1)
        self.assertEqual(len(projects), NUM_PROJECTS-1, msg=msg_amount  + "Less than Max Num Test")
        projects = Project.projects.get_projects_by_start_date(NUM_PROJECTS+1)
        self.assertEqual(len(projects), NUM_PROJECTS, msg=msg_amount + "More than Max Num Test")

        date_test = date.fromisoformat('2030-01-01')
        for i, project in enumerate(projects):
            if i != (len(projects) - 1):
                self.assertLessEqual(project.start_date, date_test,
                    msg="Project Queryset get_projects_by_start_date returned projects in the wrong order for start_date. Expect most recent first.")
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
                self.assertGreaterEqual(category.priority, priority_test,
                    msg="CV_Category Queryset get_categories_by_priority returned projects in the wrong order of priority. Expect lowest number (highest priority) first")
                priority_test = category.priority

    def test_get_categories_by_priority_with_lines(self):
        """
            Test the queryset get_categories_by_priority_with_lines
        """
        categories = CV_Category.cv_categories.get_categories_by_priority_with_lines()
        self.assertTrue(categories)

        priority_test = 0
        for i, category in enumerate(categories):
            if i != (len(categories) - 1):
                self.assertTrue(category.cv_line_set, msg="CV_Category Queryset get_categories_by_priority_with_lines returned a set without cv_lines")
                self.assertGreaterEqual(category.priority, priority_test,
                    msg="CV_Category Queryset get_categories_by_priority_with_lines returned projects in the wrong order of priority. Expect lowest number (highest priority) first")
                priority_test = category.priority

            # Hope to add order_by to prefetch later, rn too lost to care.
            # date_test = date.fromisoformat('2030-01-01')
            # for n, line in enumerate(category.cv_line_set.all()):
            #     if n != (len(category.cv_line_set.all()) - 1):
            #         self.assertLessEqual(line.start_date, date_test, msg="CV_Category Queryset get_categories_by_priority_with_lines returned cv_lines in the wrong order for start_date. Expect most recent first.")
            #         date_test = line.start_date


class CV_Line_Tests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        setup_data()

    def test_get_lines(self):
        """
            Test the queryset get_lines_full
        """
        lines = CV_Line.cv_lines.get_lines()
        self.assertTrue(lines, msg="CV_Line Queryset get_lines_full failed to return data")

    def test_get_lines_by_start_date(self):
        """
            Test the queryset get_lines_full_by_start_date
        """
        lines = CV_Line.cv_lines.get_lines_by_start_date()
        self.assertTrue(lines, msg="CV_Line Queryset get_lines_full_by_start_date failed to return data")

        date_test = date.fromisoformat('2030-01-01')
        for i, line in enumerate(lines):
            if i != (len(lines) - 1):
                self.assertLessEqual(line.start_date, date_test, msg="CV_Line Queryset get_lines_full_by_start_date returned cv_lines in the wrong order for start_date. Expect most recent first.")
                date_test = line.start_date

    def test_get_lines_for_category(self):
        """
            Test the queryset get_lines_full_for_category
        """
        categories = CV_Category.cv_categories.get_categories_by_priority()

        for category in categories:
            lines = CV_Line.cv_lines.get_lines_for_category(category.id)
            self.assertTrue(lines, msg="CV_Line Queryset get_lines_full_for_category failed to return data")
            for line in lines:
                self.assertEqual(line.category.id, category.id, msg="CV_Line Queryset get_lines_full_for_category retrieved the wrong lines")

#********* View Tests **********

class ViewNoDataTests(TestCase):

    def setup(self):
        self.client = Client()

    def test_index_no_data_response(self):
        """
            Test the index url for error free page return
        """
        response = self.client.get(reverse('resume:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resume/home.html')
        self.assertContains(response, "Oops!")

    def test_projects_no_data_response(self):
        """
            Test the index url for error free page return
        """
        response = self.client.get(reverse('resume:projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resume/projects.html')
        self.assertContains(response, "Oops!")

    def test_resume_no_data_response(self):
        """
            Test the index url for error free page return
        """
        response = self.client.get(reverse('resume:resume'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resume/resume.html')
        self.assertContains(response, "Oops!")

class ViewModelIntegrationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for view testing
        """
        setup_data()

    def setup(self):
        self.client = Client()

    def test_index_full_data_response(self):
        """
            Test the index url for error free page return with data
        """
        response = self.client.get(reverse('resume:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resume/home.html')
        self.assertTemplateUsed(response, 'resume/header_layout.html')
        self.assertTemplateUsed(response, 'resume/card_layout.html')

    def test_projects_full_data_response(self):
        """
            Test the index url for error free page return with data
        """
        response = self.client.get(reverse('resume:projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resume/projects.html')
        self.assertTemplateUsed(response, 'resume/header_layout.html')

    def test_resume_full_data_response(self):
        """
            Test the index url for error free page return with data
        """
        response = self.client.get(reverse('resume:resume'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resume/resume.html')
        self.assertTemplateUsed(response, 'resume/header_layout.html')
        self.assertTemplateUsed(response, 'resume/accordion_layout.html')
