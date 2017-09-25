from jinja2 import Environment, FileSystemLoader, select_autoescape

import importlib
import os
import stat
import hashlib

# import sys
# print(sys.path)
# exit()


def get_hash(filename):
    """Return the hexdigest of the file at filename."""
    hasher = hashlib.md5()
    with open(filename, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()


def hash_match(filename, filename2):
    """Check whether the hexdigest's of two files match."""
    return get_hash(filename) == get_hash(filename2)


def maybe_backup(temp_name, final_name, extension):
    """If the template is out of sync with the file make a backup.

    This is done through checking if the file is _readonly_ (built by template
    code) or not _readonly_ (modified by the user).
    """
    backup_name = final_name[:-len(extension)] + '.bak'

    fileAtt = os.stat(final_name)[0]
    if hash_match(final_name, temp_name):
        # Template has not been changed.
        os.remove(temp_name)
        print("Template unmodified for '{}'.".format(final_name))
    elif not fileAtt & stat.S_IWRITE:
        # File is read-only, but different from template
        # so no backup is required
        # but file should be updated!
        print("No backup required for '{}', updating!".format(final_name))
        os.remove(final_name)
        os.rename(temp_name, final_name)
    elif os.path.exists(backup_name):
        # File needs to be updated, but _not_ the backup.
        print("Updating '{}, old backup still exists!".format(backup_name))
        os.remove(final_name)
        os.rename(temp_name, final_name)
    else:
        # File is writeable, and hashes don't match and no backup exists
        # so a backup is needed!
        os.rename(final_name, backup_name)
        os.rename(temp_name, final_name)
        print("'{}' updated, old version backed up to '{}!".format(
            final_name, backup_name))
    # Set file to read only.
    os.chmod(final_name, stat.S_IREAD)


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
        temp_name = "../" + name + '.tmp'
        final_name = "../" + name + extension
        template_name = name + "_template" + extension

        # Note this is an import name so the file type is left off.
        # e.g. import profile_proficiencies_data
        data_name = name + "_data"

        data_module = importlib.import_module(data_name)
        template = env.get_template(template_name)

        data = {key: getattr(data_module, key) for key in dir(data_module) if
                key[:2] != '__'}

        # Save the newly built code.
        with open(temp_name, 'w') as file:
            file.write(template.render(**data))

        # Build a backup of all files if needed.
        maybe_backup(temp_name, final_name, extension)


if __name__ == "__main__":
    pass
