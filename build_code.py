from jinja2 import Environment, FileSystemLoader, select_autoescape

import importlib
import os
import stat

# import sys
# print(sys.path)
# exit()


def backup(filename, extension):
    """If the file has been modified by the user make a backup.

    This is done through checking if the file is _readonly_ (built by template
    code) or not _readonly_ (modified by the user).
    """
    backup_name = filename[:-len(extension)] + '.bak'

    fileAtt = os.stat(filename)[0]
    if (not fileAtt & stat.S_IWRITE):
        # File is read-only, so no backup is required
        print("No backup required for '{}'.".format(filename))
    else:
        # File is writeable, user has modified it .. so
        # make a backup
        print("Backup required for '{}'!".format(filename))
        if not os.path.exists(backup_name):
            os.rename(filename, backup_name)
            print("'{}' backed up to '{}'.".format(filename, backup_name))
        else:
            print("A backup of '{}' already exists!".format(backup_name))


def build_templates(filenames, extension):
    """For each template import the data and build a template.

    Send the data to the template as a expanded dictionary of non-builtin
    values.

    Each generate python file must exist as:
        1. a template.py composed of Jinja and Python
        2. a data file composed of pure Python
        3. and output file composed of pure Python.

    The output file is the file that the main game code will run.

    NOTE: the extention variable allows me to run '.py' or '.html' templates.
    """

    env = Environment(
        loader=FileSystemLoader(''),
        autoescape=select_autoescape(default_for_string=False, default=False)
    )

    for name in filenames:
        filename = "../" + name + extension
        template_name = name + "_template" + extension

        # Note this is an import name so the file type is left off.
        # e.g. import profile_proficiencies_data
        data_name = name + "_data"

        data_module = importlib.import_module(data_name)
        template = env.get_template(template_name)

        data = {key: getattr(data_module, key) for key in dir(data_module) if
                key[:2] != '__'}

        # Build a backup of all files if needed.
        backup(filename, extension)

        # Set file to writeable if it exists.
        try:
            os.chmod(filename, stat.S_IWRITE)
        except FileNotFoundError:
            pass

        # Save the newly built code.
        with open(filename, 'w') as file:
            file.write(template.render(**data))
        print("'{}' updated!".format(name + extension))
        # Set file to read only.
        os.chmod(filename, stat.S_IREAD)


if __name__ == "__main__":
    pass
