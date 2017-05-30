from jinja2 import Environment, FileSystemLoader, select_autoescape

import importlib
import os, stat


if __name__ == "__main__":
    """
    Usage:
    For each template import the data and build a template.
    Send the data to the template as a expanded dictionary of non-builtin
    values.    
    
    Each generate python file must exist as:
        1. a template.py/html composed of Jinja and Python or HTML
        2. a data file composed of pure Python
        3. and output file composed of Python or HTML.
        
    The output file is the file that the main game code will run.
    """
    
    env = Environment(
        loader=FileSystemLoader(''),
        autoescape=select_autoescape(default_for_string=False, default=False)
    )
    
    #This should be an automatic function! Not manual.
    names = ["profile_proficiencies"]
    
    for name in names:
        filename = "../" + name + ".html"
        template_name = name + "_template.html"
        
        #Note this is an import name so the file type is left off.
        #e.g. import profile_proficiencies_data
        data_name = name + "_data" 
        
        data_module = importlib.import_module(data_name)
        template = env.get_template(template_name)

        #Loads all variables declared in module.
        #Which are then passed to the template.
        data = {key: getattr(data_module, key) for key in dir(data_module) if key[:2] != '__'}
        
        #Set file to writeable if it exists.
        try:
            os.chmod(filename, stat.S_IWRITE)
        except FileNotFoundError:
            pass

            
        #Need to add a backup section.
        #And save the old file as *.bak
        #But don't overwrite old .bak files? Or just make *.bak2, *.bak3 etc.

        
        #Save the newly built code.
        with open(filename, 'w') as file:
            file.write(template.render(**data))
        
        #Set file to read only.
        os.chmod(filename, stat.S_IREAD)
