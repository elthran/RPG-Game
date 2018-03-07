import os
import pytest
from pprint import pprint
import sys
import os

try:
    import build_code
except ImportError:
    # Get the name of the current directory for this file and split it.
    old_path = os.path.dirname(os.path.abspath(__file__)).split(os.sep)
    new_path = os.sep.join(old_path[:-1])
    # -1 refers to how many levels of directory to go up
    sys.path.insert(0, new_path)
    import build_code
    sys.path.pop(0)


class TestBuildCode:
    def test_if_vs_try(self):
        all_templates = {}
        all_templates2 = {}

        old_path = os.path.dirname(os.path.abspath(__file__)).split(os.sep)
        current_dir = os.sep.join(old_path[:-1])
        assert current_dir.endswith('RPG-Game')
        for root, dirs, files in os.walk(current_dir):
            # Check if the parent dir is an 'abstraction_lv*' dir.
            if root.split(os.sep)[-1].startswith("abstraction_lv"):
                for file in files:
                    if "_template" in file:
                        name, extension = file.rsplit(sep='.', maxsplit=1)
                        try:
                            all_templates[root][extension].append(name)
                        except KeyError:
                            try:
                                all_templates[root][extension] = [name]
                            except KeyError:
                                all_templates[root] = {extension: [name]}

                        if root in all_templates2:
                            if extension in all_templates2[root]:
                                all_templates2[root][extension].append(name)
                            else:
                                all_templates2[root][extension] = [name]
                        else:
                            all_templates2[root] = {extension: [name]}

        assert all_templates == all_templates2
