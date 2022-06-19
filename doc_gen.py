import pathlib
import os
from os import listdir, walk, chdir
from os.path import isfile, join

####### Global Variables #############
# Varible used to track the project name
project_name = 'portfoliosite'
# Variable used to tell doc_gen which modules to document
django_modules = ['resume', 'portfolio_music_player']
# Variable used to let doc_gen know where the global templates are stored
global_templates = ['templates/']
# Global variable used to add scss paths from which documentation can be retrieved
scss_paths = ['scss/']
#Variable controlling where the docs folder is located
docs_loc = 'docs/source/'
# List of directory names to exclude from python module list
py_exclude_dirs = ['migrations', '__pycache__']

def get_overview_comment(file, comment_start, comment_end):
    """
        Takes in a file, a substring to search for the start of an overview comment,
        and a substring to search for the end of an overview comment. Returns the overview comment
        in the given file.
    """
    doc_string = None

    with open(file) as f:
        doc_string = f.read()

    if comment_start in doc_string:
        start_index = doc_string.rindex(comment_start) + len(comment_start)
        end_index = doc_string.index(comment_end, start_index)
        return doc_string[start_index:end_index]

    return doc_string

def generate_django_index_rst_files():
    """ Generates the index.rst files for included django modules
    """
    base = """
    .. toctree::
       :maxdepth: 2
       :caption: Contents:
       :glob:
    """
    django_docs = f'../{docs_loc}django/'
    gen_list = django_modules.copy()
    gen_list.append(project_name)

    # Change the working directory for Django docs
    pwd = os.getcwd()
    chdir('portfoliosite')

    for module in gen_list:
        pathlib.Path(f'{django_docs}{module}').mkdir(parents=True, exist_ok=True)
        with open(f'{django_docs}{module}/index.rst', "w") as f:
            title_restruc = '='*len(module)
            mod_string = f'{module}\n{title_restruc}\n\n{base}\n\n       {module}*\n       templates'
            f.write(mod_string)

    chdir(pwd)

def doc_python_modules():
    """
        Generates an rst file for autodoc based
        on the available python modules located with
        each app listed in django_modules.
    """
    django_docs = f'../{docs_loc}django/'

    # Change the working directory for Django docs
    pwd = os.getcwd()
    chdir('portfoliosite')

    for module in django_modules:
        files = []
        for (dir_path, dir_names, file_names) in walk(module):
            if not any(dir in dir_path for dir in py_exclude_dirs):
                for file in file_names:
                    if '.py' in file:
                        dir_path = dir_path.replace('/', '.')
                        files.append(f'{dir_path}.{file[:-3]}')

        pathlib.Path(f'{django_docs}{module}').mkdir(parents=True, exist_ok=True)
        for file in files:
            title_restruc = '='*len(file)
            rst = f'{file}\n{title_restruc}\n\n.. automodule:: {file}\n    :members:'
            with open(f'{django_docs}{module}/{file}.rst', "w") as f:
                f.write(rst)

    chdir(pwd)

def doc_django_templates():
    """
        Retireves the "Overview" comment from templates, if available,
        and turns it into html documentation.
    """
    django_docs = f'../{docs_loc}django/'
    #put together necessary template paths
    template_paths = [s + '/templates/' + s + '/' for s in django_modules]
    template_paths.extend(global_templates)

    # Change the working directory for Django docs
    pwd = os.getcwd()
    chdir('portfoliosite')

    #Retrieve template files
    for path in template_paths:
        doc_data = {
            'app_name': '',
            'templates': [],
        }
        files = []
        files.extend([join(path, f) for f in listdir(path) if isfile(join(path, f))])

        doc_data['app_name'] = path[ 0:(path.index("/")) ]
        if doc_data['app_name'] == "templates":
            doc_data['app_name'] = project_name

        # Retrieve overview string and create an html page
        for file in files:
            doc_string = get_overview_comment(file, '{% comment "Overview" %}', '{% endcomment %}')
            doc_data['templates'].append([ file[(file.rindex("/")+1):len(file)], doc_string])

        # Setup the rst for output
        temp_str = ' templates'
        title_restruc = '='*(len(doc_data["app_name"]) + len(temp_str))
        rst = f'{doc_data["app_name"]}{temp_str}\n{title_restruc}\n\n'
        for template in doc_data['templates']:
            title_restruc = '-'*len(template[0])
            rst += f'{template[0]}\n{title_restruc}\n{template[1]}\n\n'

        pathlib.Path(f'{django_docs}{doc_data["app_name"]}').mkdir(parents=True, exist_ok=True)
        with open(f'{django_docs}{doc_data["app_name"]}/templates.rst', "w") as f:
            f.write(rst)

    chdir(pwd)

def doc_scss():
    """ Generates rst files for sphinx to use when documenting the projects scss
    """
    doc_string = None
    scss_docs = f'{docs_loc}scss/'
    files = []

    for path in scss_paths:
        files.extend([join(path, f) for f in listdir(path) if isfile(join(path, f))])

    for file in files:
        filename = file[(file.rindex("/")+1):len(file)]
        title_restruc = '='*len(filename)
        rst = f'{filename}\n{title_restruc}\n\n{get_overview_comment(file, "/* @overview", "*/")}'
        pathlib.Path(scss_docs).mkdir(parents=True, exist_ok=True)
        with open(f'{scss_docs}{filename}.rst', "w") as f:
            f.write(rst)

generate_django_index_rst_files()
doc_python_modules()
doc_django_templates()
doc_scss()
