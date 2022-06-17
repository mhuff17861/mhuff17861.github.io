resume templates
==========

projects.html
------------

    This is template generates a projects page. It extends header_layout to
    provide a header and slide_layout to provide slides for recent projects. Check those
    layouts to determine what data the template should be given.


home.html
------------

    This is template generates a home page. It extends header_layout to
    provide a header and card_layout to provide cards for recent projects. Check those
    layouts to determine what data the template should be given.


resume.html
------------

    This is template generates a resume page. It extends header_layout to
    provide a header and accordion_layout to provide and accordion for cv lines.
    Check those layouts to determine what data the template should be given.


card_layout.html
------------

    This is a generalized card layout. It expects a list of card data
    called "cards," with each card containing a value for title, body,
    image, and image_alt_text. The image must contain a url (card.image.url)
    which points to the media that will be loaded.

    Optionally, a url and url_title can be provided which will be used to create
    a button on the bottom of the card.

    This template accepts markdown via the markdown_extras template tag.


accordion_layout.html
------------

    This is a generalized accordion layout. It expects a list of categories
    called "accordion_categories" in which each category contains a name
    and a list of items (category.items). Each item should have a value called
    entry, which will be placed under each accordion category.

    This template accepts markdown via the markdown_extras template tag.


header_layout.html
------------

    This is a generalized header layout. It expects a header which contains
    values for title, alignment, body, image, and image_alt_text. The image must contain a
    url (header.image.url) that links to the media to be displayed. The alignment can
    have the values of C, L, and R, which direct the position of the image to the
    center, left, and right respectively. If not alignment is provided, the default
    is to the left.

    This template accepts markdown via the markdown_extras template tag.


slide_layout.html
------------

    This is a generalized slide layout. It expects a list of slides, with
    each slide containing a value for title, body, image, and image_alt_text.
    The image value must contain value for url (slide.image.url) linking to
    the desired media to be displayed.

    The slides alternate between the image being on the left or right side. 

    This template accepts markdown via the markdown_extras template tag.


