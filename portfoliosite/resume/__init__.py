import os
if os.environ.get("CI_MAKING_DOCS") is not None:
    # pdoc will not work with django unless you first call django.setup().
    # Unfortunately, calling that function in an __init__ file means that
    # django will crash if actually run, so only execute the following if
    # we are generating docs
    # https://github.com/pdoc3/pdoc/issues/314
    # Template command: CI_MAKING_DOCS=1 pdoc app/module.py

    # Ignore a few directories
    __pdoc__ = {}
    __pdoc__["migrations"] = False

    import django
    django.setup()
