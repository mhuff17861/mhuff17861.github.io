"""
    This file does any initial setup work needed to run Django/generate documentation.

    Sphinx will not work with django unless you first call django.setup().
    Unfortunately, calling that function in an __init__ file means that
    django will crash if actually run, so only execute the following if
    we are generating docs. It does so by checking for the CI_MAKING_DOCS environment
    variable.
"""
import os
import logging

logger = logging.getLogger(__name__)

if os.environ.get("CI_MAKING_DOCS") is not None:
    import django
    try:
        django.setup()
    except RuntimeError:
        logger.warning("Django is already setup.")
