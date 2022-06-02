# blog/templatetags/markdown_extras.py
from django import template
from django.template.defaultfilters import stringfilter

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
import markdown as mdown

register = template.Library()

# *************** Extensions ************
DEFAULT_A_COLOR = "link-light"

class LinkColorProcessor(Treeprocessor):
    """
        A processor which adds the appropriate link color to
        every link in the processed markdown
    """
    def run(self, root):
        def set_link_class(element):
            """
                Modifies the color of the link class to fit within the color scheme
            """
            for child in element:
                if child.tag == "a":
                    child.set("class", DEFAULT_A_COLOR) #set the class attribute
                set_link_class(child) # run recursively on children

        set_link_class(root)

class LinkColorExtension(Extension):
    """
        An extension which uses LinkColorProcessor to add
        the appropriate link color to every link in the processed markdown
    """
    def extendMarkdown(self, md, key='link_color', index=0):
        md.registerExtension(self)
        md.treeprocessors.register(LinkColorProcessor(md.parser), key, index)


@register.filter()
@stringfilter
def markdown(value):
    """
        Filter which includes basic python markdown and the LinkColorExtension
    """
    return mdown.markdown(value, extensions=['markdown.extensions.fenced_code', LinkColorExtension()])
