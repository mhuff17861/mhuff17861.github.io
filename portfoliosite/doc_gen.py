import pathlib
from os import listdir
from os.path import isfile, join
import pdoc
from pdoc import html_helpers, Doc, Module

####### Global Variables #############
# Variable used to tell doc_gen which modules to document
django_modules = ['resume', 'portfolio_music_player']
# Variable used to let doc_gen know where the global templates are stored
global_templates = ['templates/']
#Variable controlling where the docs folder is located
docs_loc = '../docs/'

def recursive_htmls(mod):
    yield mod.name, mod.html()
    for submod in mod.submodules():
        yield from recursive_htmls(submod)

def doc_python_modules():
    """
    Documents the django python files
    """
    # pdoc setup
    context = pdoc.Context()

    modules = [pdoc.Module(mod, context=context)
               for mod in django_modules]
    pdoc.link_inheritance(context)
    for mod in modules:
        # Create an appropriate doc directory
        pathlib.Path(f'{docs_loc}{mod.name}').mkdir(parents=True, exist_ok=True)

        for module_name, html in recursive_htmls(mod):
            module_name_split = module_name.split('.')

            # Checks length of the name to determine the appropriate directory to output the
            # html in so all the links will work.
            if len(module_name_split) == 1:
                with open(f'{docs_loc}{mod.name}/index.html', "w") as file:
                    file.write(html)
            elif len(module_name_split) == 2:
                # This check verifies whether a module should have it's own folder
                # If so, the page generated must also be called index.html for generated links to work.
                if "submodules" in html:
                    pathlib.Path(f'{docs_loc}{mod.name}/{module_name_split[-1]}/').mkdir(parents=True, exist_ok=True)
                    with open(f'{docs_loc}{mod.name}/{module_name_split[-1]}/index.html', "w") as file:
                        file.write(html)
                else:
                    with open(f'{docs_loc}{mod.name}/{module_name_split[-1]}.html', "w") as file:
                        file.write(html)
            elif len(module_name_split) >= 2:
                # This section will create the appropriate directories/names for all
                # modules deeper than 2 directories.
                dir = ''
                for name in reversed(module_name_split):
                    # This check verifies whether a module should have it's own folder
                    # If it shouldn't, the loop iteration is skipped.
                    if name == module_name_split[-1] and "submodules" not in html:
                        continue
                    dir = name + '/' + dir
                dir = docs_loc + dir
                pathlib.Path(dir).mkdir(parents=True, exist_ok=True)

                # This check verifies whether a module should be called index.html
                # for generated links to work.
                if "submodules" in html:
                    with open(f'{dir}index.html', "w") as file:
                        file.write(html)
                else:
                    with open(f'{dir}{module_name_split[-1]}.html', "w") as file:
                        file.write(html)

def get_template_overview_comment(file):
    """
        Takes in a Django template html file and returns
        the contents of the multiline comment labeled 'Overview'
    """
    doc_string = None
    comment_start = '{% comment "Overview" %}'
    comment_end = '{% endcomment %}'

    with open(file) as f:
        doc_string = f.read()

    if comment_start in doc_string:
        start_index = doc_string.rindex(comment_start) + len(comment_start)
        end_index = doc_string.index(comment_end, start_index)
        return doc_string[start_index:end_index]

    return doc_string


def doc_templates():
    """
        Retireves the "Overview" comment from templates, if available,
        and turns it into html documentation.
    """
    #put together necessary template paths
    template_paths = [s + '/templates/' + s + '/' for s in django_modules]
    template_paths.extend(global_templates)

    #Retrieve template files
    for path in template_paths:
        files = []
        files.extend([join(path, f) for f in listdir(path) if isfile(join(path, f))])

        app_name = path[ 0:(path.index("/")) ]
        if app_name == "templates":
            app_name = "global"


        html = f'<h1>{app_name}</h1>'
        # Retrieve overview string and create an html page
        for file in files:
            doc_string = get_template_overview_comment(file)
            doc_html = f'<h2>{file[ (file.rindex("/")+1):len(file) ]}</h2>' + html_helpers.to_html(doc_string)
            html += doc_html

        pathlib.Path(f'{docs_loc}templates/').mkdir(parents=True, exist_ok=True)
        with open(f'{docs_loc}templates/{app_name}.html', "w") as f:
            f.write(html)


doc_python_modules()
doc_templates()
