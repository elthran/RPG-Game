import importlib
import os
import stat
import hashlib
from contextlib import contextmanager
import sys
import re

from pprint import pprint
import pdb

import jinja2
from jinja2 import Environment

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


# A custom Jinja2 template loader that removes the extra indentation
# of the template blocks so that the output is correctly indented
# Compliments of https://blog.kangz.net/posts/2016/08/31/code-generation-the-easier-way/
class PrependIndentLoader(jinja2.BaseLoader):
    """A class to remove the indent added by template blocks code.

    This occurs before the code is processed by Jinja regular.
    Usage:
        env = Environment(
        loader=PrependIndentLoader(''),
        trim_blocks=True,
        lstrip_blocks=True,
        )

    NOTE: trim_blocks=True and lstrip_blocks=True are also required!
    """
    blockstart = re.compile('{%-?\s*(if|for|block)[^}]*%}')
    blockend = re.compile('{%-?\s*end(if|for|block)[^}]*%}')

    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        path = os.path.join(self.path, template)
        if not os.path.exists(path):
            raise jinja2.TemplateNotFound(template)
        mtime = os.path.getmtime(path)
        with open(path) as f:
            source = self.preprocess(f.read())
        return source, path, lambda: mtime == os.path.getmtime(path)

    def preprocess(self, source):
        lines = source.split('\n')

        # Compute the current indentation level of the template blocks and remove their indentation
        result = []
        end_match, start_match = None, None
        indent_level = 0

        for line in lines:
            # We don't want to remove quite as much indent from the end
            # tag so we subtract 1 indent level
            end_match = self.blockend.search(line)
            if end_match:
                indent_level -= 1
                # indent_level = self.blockend.search(line).start() // 4 - 1

            result.append(self.remove_indentation(line, indent_level))

            # The reverse order (searching for blockstart at the bottom of
            # the loop) is essentially to simulate a 'do while loop'.
            # The assumption is that the main content will never be indented
            # before at least one template tag is found ... so the first
            # iteration of the loop will only ever execute this last line.
            start_match = self.blockstart.search(line)
            if start_match:
                indent_level += 1
                # indent_level = self.blockstart.search(line).start() // 4 - 1

        # print('\n'.join(result))
        # pdb.set_trace()
        return '\n'.join(result)

    def remove_indentation(self, line, n):
        for _ in range(n):
            # pdb.set_trace()
            if line.startswith(' '):
                line = line[4:]
            elif line.startswith('\t'):
                line = line[1:]
            else:
                assert(line.strip() == '')
        return line


def fix_camel_case(name):
    """Detect and fix camel case names.

    Otherwise these names will be lost when converting to 'title()'.
    """
    if name[0].isupper() and name[1:].islower():
        return name
    print("Bad name:", name)
    fixed_name = name[0] + ''.join([" " + letter.lower()
                                    if (index > 0 and letter.isupper())
                                    else letter
                                    for index, letter in enumerate(name[1:])])
    print("Fixed name:", fixed_name)
    return fixed_name


def get_names(names):
    """Pull the first item from a more complex list of data.

    Fix the naming scheme if it use camel case an use human readable instead.
    """
    sorted_names = sorted([name[0] for name in names])
    return [fix_camel_case(name) for name in sorted_names]


def normalized_attrib_names(names):
    """Normalize names for columns."""
    return [name.lower().replace(" ", "_") for name in names]


def normalized_class_name(name):
    """Normalized name for class."""
    return name.title().replace(" ", "")


def normalized_class_names(names):
    """Normalized names for classes."""
    return [normalized_class_name(name) for name in names]


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
    first_run = False

    try:
        fileAtt = os.stat(final_name)[0]
    except FileNotFoundError:
        first_run = True

    if first_run:
        os.rename(temp_name, final_name)
        print("New file '{}' created!".format(final_name))
    elif hash_match(final_name, temp_name):
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
        loader=PrependIndentLoader(''),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    env.globals['get_names'] = get_names
    env.globals['normalized_attrib_names'] = normalized_attrib_names
    env.globals['normalized_class_name'] = normalized_class_name
    env.globals['normalized_class_names'] = normalized_class_names

    for name in filenames:
        temp_name = "../" + name + '.tmp'
        final_name = "../" + name + extension
        template_name = name + "_template" + extension

        template = env.get_template(template_name)

        # Note this is an import name so the file type is left off.
        # e.g. import profile_proficiencies_data
        data_name = name + "_data"
        data = {}
        try:
            data_module = importlib.import_module(data_name)
            data = {key: getattr(data_module, key)
                    for key in dir(data_module)
                    if key[:2] != '__'}
        except ImportError:
            print("No data module named {}".format(data_name + '.py'))

        # Output a header.
        comment = LANGUAGES[extension]['multi_line_comment']
        with open(temp_name, 'w') as file:
            file.write('''{}
This file is generated by 'build_code.py'.
It has been set to read only so that you don't edit it without using
'build_code.py'. Thought that may change in the future.
{}\n\n
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
