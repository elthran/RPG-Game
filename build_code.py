from jinja2 import Environment, FileSystemLoader, select_autoescape

import importlib
import os
import stat
import hashlib
from contextlib import contextmanager
import sys

LANGUAGES = {
    '.html': {
        'multi_line_comment': {
            'start': "<!--",
            'end': "-->",
        },
    },
    '.py': {
        'multi_line_comment': {
            'start': '"""',
            'end': '"""',
        },
    },
}


def fix_camel_case(name):
    """Detect and fix camel case names.

    Otherwise these names will be lost when converting to 'title()'.
    """
    if name[0].isupper() and name[1:].islower():
        return name
    # print("Bad name:", name)
    fixed_name = name[0] + ''.join([" " + letter.lower()
                                    if (index > 0 and letter.isupper())
                                    else letter
                                    for index, letter in enumerate(name[1:])])
    # print("Fixed name:", fixed_name)
    return fixed_name


def get_names(names):
    """Pull the first item from a more complex list of data.

    Fix the naming scheme if it use camel case an use human readable instead.
    """
    sorted_names = sorted([name[0] for name in names])
    return [fix_camel_case(name) for name in sorted_names]


def normalize_attrib_name(name):
    """Normalize name to Python attribute style.

    Convert "First strike" to "first_strike"
    """
    return fix_camel_case(name).lower().replace(" ", "_")


def normalize_attrib_names(names):
    """Normalize names for columns."""
    return [normalize_attrib_name(name) for name in names]


def normalize_class_name(name):
    """Normalized name for class."""
    return fix_camel_case(name).title().replace(" ", "")


def normalize_class_names(names):
    """Normalized names for classes."""
    return [normalize_class_name(name) for name in names]


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
        os.chmod(final_name, stat.S_IWRITE)
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

    # Fix extension so it always includes the period.
    if extension[0] != '.':
        extension = "." + extension

    env = Environment(
        loader=FileSystemLoader(''),
        autoescape=select_autoescape(default_for_string=False, default=False),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    env.globals['get_names'] = get_names
    env.globals['normalize_attrib_name'] = normalize_attrib_name
    env.globals['normalize_attrib_names'] = normalize_attrib_names
    env.globals['normalize_class_name'] = normalize_class_name
    env.globals['normalize_class_names'] = normalize_class_names

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

        # Output a header.
        comment = LANGUAGES[extension]['multi_line_comment']
        with open(temp_name, 'w') as file:
            file.write('''{}
This file is generated by 'build_code.py'.
It has been set to read only so that you don't edit it without using
'build_code.py'. Thought that may change in the future.
{}\n
'''.format(comment['start'], comment['end']))
        # Save the newly built code.
        with open(temp_name, 'a') as file:
            template.stream(**data).dump(file)

        # Build a backup of all files if needed.
        maybe_backup(temp_name, final_name, extension)


@contextmanager
def pushd_popd(new_dir):
    """Wrap a command in pushd popd statements.

    In English:
    1. Change to a new directory.
    2. Do something.
    3. Go back (and always go back).
    Thanks to https://stackoverflow.com/a/13847807/488331

    Also adds new dir to path and removes it afterwards.
    """
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    sys.path.insert(0, new_dir)
    try:
        yield
    finally:
        sys.path.pop(0)
        os.chdir(previous_dir)


def get_all_templates_by_dir_then_extension():
    """Return a dictionary of all templates.

    This dictionary looks like:
    d = {
        absolute_folder: {
            'py': [file1, file2],
            'html: [file3, files4]
        }
        absolute_folder2: {
            'py: [file5, file6]
            'ext3': [file7, file8]
        }
    }
    Or it should anyways :P
    
    NOTE: this should be run from the RPG-game folder. Or it won't work right.
    Or maybe not? I don't know these things.
    """
    
    templates = {}
    current_dir = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(current_dir):
        # Check if the parent dir is an 'abstraction_lv*' dir.
        if root.split(os.sep)[-1].startswith("abstraction_lv"):
            for file in files:
                try:
                    name, extension = file.rsplit(sep='.', maxsplit=1)
                except ValueError:
                    continue
                if name.endswith("_template"):
                    # Remove the _template from the end of the file name.
                    name = name.replace("_template", "")
                    try:
                        templates[root][extension].append(name)
                    except KeyError:
                        try:
                            templates[root][extension] = [name]
                        except KeyError:
                            templates[root] = {extension: [name]}
    return templates


def deepest_first(templates_dict):
    """Return the key list with the longest one first.

    This should allow for multiple levels of abstraction to be executed
    from deepest first ... :)
    """
    return sorted((key for key in templates_dict), reverse=True)


if __name__ == "__main__":
    """Build all templates in the game at all abstraction levels.
    
    I don't think I have fixed the order yet ..
    """

    all_templates = get_all_templates_by_dir_then_extension()

    for dir_ in deepest_first(all_templates):
        with pushd_popd(dir_):
            file_names = all_templates[dir_]
            for extension, names in file_names.items():
                build_templates(names, extension)
    print("Code updated!")
