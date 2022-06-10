import pathlib
import pdoc

modules = ['resume']  # Public submodules are auto-imported
context = pdoc.Context()

modules = [pdoc.Module(mod, context=context)
           for mod in modules]
pdoc.link_inheritance(context)

def recursive_htmls(mod):
    yield mod.name, mod.html()
    for submod in mod.submodules():
        yield from recursive_htmls(submod)

for mod in modules:
    pathlib.Path(f'docs/{mod.name}').mkdir(parents=True, exist_ok=True)
    for module_name, html in recursive_htmls(mod):
        module_name_split = module_name.split('.')
        print(module_name_split)

        # Checks length of the name to determine the appropriate directory to output the
        # html in so all the links will work.
        if len(module_name_split) == 1:
            with open(f'docs/{mod.name}/index.html', "w") as file:
                file.write(html)
        elif len(module_name_split) == 2:
            # This check verifies whether a module should have it's own folder
            # If so, the page generated must also be called index.html for generated links to work.
            if "submodules" in html:
                pathlib.Path(f'docs/{mod.name}/{module_name_split[-1]}/').mkdir(parents=True, exist_ok=True)
                with open(f'docs/{mod.name}/{module_name_split[-1]}/index.html', "w") as file:
                    file.write(html)
            else:
                with open(f'docs/{mod.name}/{module_name_split[-1]}.html', "w") as file:
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
            dir = 'docs/' + dir
            pathlib.Path(dir).mkdir(parents=True, exist_ok=True)

            # This check verifies whether a module should be called index.html
            # for generated links to work.
            if "submodules" in html:
                with open(f'{dir}index.html', "w") as file:
                    file.write(html)
            else:
                with open(f'{dir}{module_name_split[-1]}.html', "w") as file:
                    file.write(html)
