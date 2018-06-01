# Explanation of this MVC implementation

The new format of the code should work like this:

* All game objects should go in the 'models' package.

* All app.routes should go in the 'routes' package. Views should only manipulate the display of information.

* For each 'view' there should be a 'controller' package module. The controller should allow for any action in the game to be enacted via python interpreter.
e.g.
```python
>>> explore_dungeon(hero)  # should have this hero explore a dungeon.
```

* The 'services' package contains any functions that might be used in multiple locations.

* 'policies' should enact CRUD security features in the game (once I find out how) CRUD - Create Read Update Delete (database data interactions)

* 'controler/commands' package should probably be redone ... but right now it is all the python command code from before. Each method should have it's own file.

* 'interfaces' package is a design pattern ... that allows extensible object behavior.

* 'models/database' package handles the database backend.

* 'models/relationships' package ... could implement relationships between models. Might be changed to 'provides' package instead ..?

* 'rpg_game_tests' package test all the code. Each 'controller' method should have it's own set of tests.


* 'elthranonline' package - 'app.py' has been moved (in its minimalist form) to the '__init__.py' file. The 'templates' and 'static' folders are in here now.

### Extra note:
Each 'template', 'view' and 'controller' function should have it's own file
with the SAME name.
e.g.
* view\login.py
* controller\login.py
* elthranonline\templates\login.html
tests\test_controller\test_login.py  # not finalized
