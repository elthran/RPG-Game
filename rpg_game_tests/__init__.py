# from .test_helpers import GenericTestCase
from .test_helpers import db_execute_script
from .test_helpers import Mock

"""
HelpMe! This package uses relative imports.
If you want to import the modules in a nearby package
e.g.

file - 'test_hero.py'
use: from . import GenericTestCase

To allow any file to correctly import these you would use:
from rpg_game_tests import GenericTestCase

You need to add any new modules to list of _relative_ (note the leading .)
imports at the top of this file.
"""
