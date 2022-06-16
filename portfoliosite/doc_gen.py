import pathlib
from os import listdir, walk
from os.path import isfile, join

####### Global Variables #############
# Variable used to tell doc_gen which modules to document
django_modules = ['resume', 'portfolio_music_player']
# Variable used to let doc_gen know where the global templates are stored
global_templates = ['templates/']
#Variable controlling where the docs folder is located
docs_loc = '../docs/source/'
# List of directory names to exclude from python module list
py_exclude_dirs = ['migrations', '__pycache__']


def doc_python_modules():
    """
        Generates an rst file for autodoc based
        on the available python modules located with
        each app listed in django_modules.
    """
    for module in django_modules:
        files = []
        for (dir_path, dir_names, file_names) in walk(module):
            if not any(dir in dir_path for dir in py_exclude_dirs):
                for file in file_names:
                    if '.py' in file:
                        dir_path = dir_path.replace('/', '.')
                        files.append(f'{dir_path}.{file[:-3]}')

        pathlib.Path(f'{docs_loc}django/{module}').mkdir(parents=True, exist_ok=True)
        for file in files:
            rst = f'{file}\n==========\n\n.. automodule:: {file}\n    :members:'
            with open(f'{docs_loc}django/{module}/{file}.rst', "w") as f:
                f.write(rst)


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
        doc_data = {
            'app_name': '',
            'templates': [],
        }
        files = []
        files.extend([join(path, f) for f in listdir(path) if isfile(join(path, f))])

        doc_data['app_name'] = path[ 0:(path.index("/")) ]
        if doc_data['app_name'] == "templates":
            doc_data['app_name'] = "portfoliosite"

        # Retrieve overview string and create an html page
        for file in files:
            doc_string = get_template_overview_comment(file)
            doc_data['templates'].append([ file[(file.rindex("/")+1):len(file)], doc_string])

        # Setup the rst for output
        rst = f'{doc_data["app_name"]} templates\n==========\n\n'
        for template in doc_data['templates']:
            rst += f'{template[0]}\n------------\n{template[1]}\n\n'

        pathlib.Path(f'{docs_loc}django/{doc_data["app_name"]}').mkdir(parents=True, exist_ok=True)
        with open(f'{docs_loc}django/{doc_data["app_name"]}/templates.rst', "w") as f:
            f.write(rst)


doc_python_modules()
doc_templates()
