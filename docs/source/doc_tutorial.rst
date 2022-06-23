Documentation tutorial
=======================

doc_gen.py Docs
-----------------

doc_gen.py generates rst files which use Sphinx's automodule function to create documentation. In order
to add/modify documentation for doc_gen.py, simply add/remove/modify the docs strings throughout the
Python file.

Django Python Docs
-------------------

doc_gen.py generates rst files which use Sphinx's automodule function to create documentation. It decides which modules to import based
on the contens of project_name and the django_modules list.

In order to add/modify documentation for included Django Python files, simply add/remove/modify the docs strings throughout each
Python file.

Django Template Docs
-------------------------

doc_gen.py generates rst files for each template based on the first comment marked "Overview" in the template. It decides which modules to import based
on the contens of project_name and the django_modules list.

In order to add/modify documentation for a file, you must modify the "Overview" comment in the file.

Ex::

  {% comment "Overview" %}
  This is the comment that will be used to generate the rst file.

  -  You can include your own
  -  rst syntax in the comment if you wish.
  {% endcomment %}

SCSS Docs
------------
doc_gen.py generates rst files for each SCSS file based on the first multiline comment marked @overview. It looks for scss files
in all of the paths listed in the scss_paths list variable.

In order to add/modify documentation for a file, you must modify the @overview comment in the file.

Ex::

  /* @overview
  This is the comment that will be used to generate the rst file.

  -  You can include your own
  -  rst syntax in the comment if you wish.
  */
