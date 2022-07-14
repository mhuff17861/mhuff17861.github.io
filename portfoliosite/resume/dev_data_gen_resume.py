"""
    This file is used to quickly setup data for the resume app based on what factory.py can generate.
    It is definitely not perfect, but requires no manual data entry on the part of the developer, meaning that
    non-automated testing can proceed much faster when developing new apps/views/etc.

    Usage:
    -------------

    To use, simply run the python script via the django shell.
    ``python manage.py shell < resume/dev_data_gen_resume.py``
"""

from resume.factories import *
import os
import logging

def setup_data():
    """
        Sets up data that can be used to test every model/view in a development environment.
    """
    NUM_PROJECTS = 5
    """Sets the number of projects to be generated"""
    NUM_CV_CATEGORIES = 10
    """Sets the number of CV_Categories to be generated"""
    NUM_CV_LINES = 10
    """Sets the number of CV_Lines per CV_Category to be generated"""

    # Make sure generation doesn't run for documentation generation.
    if os.environ.get("CI_MAKING_DOCS") is None:
        logger.debug(f"Generating Resume development data.")
        user = UserFactory.create()
        PageHeaderFactory.create_batch(len(Page_Header.PAGE_CHOICES), user_id=user)
        ProjectFactory.create_batch(NUM_PROJECTS, user_id=user)
        categories = CVCategoryFactory.create_batch(NUM_CV_CATEGORIES, user_id=user)

        for i, category in enumerate(categories):
            cv_lines = CVLineFactory.create_batch(NUM_CV_LINES, category=category, user_id=user)

setup_data()
