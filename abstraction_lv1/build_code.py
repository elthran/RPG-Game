from jinja2 import Environment, FileSystemLoader, select_autoescape

import importlib
import os
import stat


# Not built!
# Need to add a backup section.
# And save the old file as *.bak
# But don't overwrite old .bak files? Or just make *.bak2, *.bak3 etc.
def backup(filename):
    if '.bak' in filename:
        pass
    os.path.isfile(path)


if __name__ == "__main__":
    """
    Usage:
    For each template import the data and build a template.
    Send the data to the template as a expanded dictionary of non-builtin
    values.    
    
    Each generate python file must exist as:
        1. a template.py composed of Jinja and Python
        2. a data file composed of pure Python
        3. and output file composed of pure Python.
        
    The output file is the file that the main game code will run.
    """
    
    env = Environment(
        loader=FileSystemLoader(''),
        autoescape=select_autoescape(default_for_string=False, default=False)
    )
    
    # This should be an automatic function! Not manual.
    names = ["attributes", "proficiencies", "complex_relationships",
             "abilities"]
    
    for name in names:
        filename = "../" + name + ".py"
        template_name = name + "_template.py"
        data_name = name + "_data"
        
        data_module = importlib.import_module(data_name)
        template = env.get_template(template_name)

        data = {key: getattr(data_module, key) for key in dir(data_module) if key[:2] != '__'}
        
        # Set file to writeable if it exists.
        try:
            os.chmod(filename, stat.S_IWRITE)
        except FileNotFoundError:
            pass

        # Need to add a backup section.
        # And save the old file as *.bak
        # But don't overwrite old .bak files? Or just make *.bak2, *.bak3 etc.
        # try:
        #     if os.path.isfile(path):
        #         os.rename(filename, filename + '.bak')
        # except FileNotFoundError:
        #     pass


        
        # Save the newly built code.
        with open(filename, 'w') as file:
            file.write(template.render(**data))
        print("{} updated!".format(name + ".py"))
        # Set file to read only.
        os.chmod(filename, stat.S_IREAD)
