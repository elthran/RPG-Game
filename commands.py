import pdb

from flask import render_template_string
from engine import Engine


class Command:
    """Run a list of html update commands based on the string cmd.
    
    Usage:
    in app.py
    
    from commands import Command
    
    @app.route('/<cmd>')
    def command(cmd=None):
        try:
            # command_function = getattr(Command, <cmd>)
            # response = command_function(hero, database,
            #   javascript_kwargs_from_html)
            command_function = Command.cmd_functions(cmd)
            try:
                response = command_function(hero, database=database,
                                            arg_dict=request.args)
                database.update()
                # pdb.set_trace()
                return response
            except Exception as ex:
                raise ex
        except AttributeError:
            print("Warning: Using old code for command: '{}'".format(cmd))
            print("You need to write a static function called '{}' in "
                  "commands.py in the Command class.".format(cmd))
            # Look in the not yet refactored list of if statements ...

    This should call the function and execute it in the Command class.

    The format for a button is:
    -<button data-py-function="consume" data="{{ item.id }}"
    data-js-callback="javascript_consume"></button>
    -Where data-py-function means this object runs command code.
    -Where data is the python object's database id. Or any other data necessary.
    -Where data-py-function="consume" is the name of the Python
        method/function to run (in commands.py).
    -Where data-js-callback="javascript_consume" is the name of a JavaScript
        function that accepts data as a return value from the Python
        function defined in data-py-function="..".
        NOTE: This function runs after the python code returns a response.
        "onClick" does not. It runs first/or independently?

    Usage:
        Use the python functions if you need to change the database or hero
        object.
        Use the JS functions if you need to update the website data.
            e.g. buy and item ... send it to the python code with the item's id
        Drop hero's gold ... add item to inventory.
        Then send back the confirmation to the JS function and update the hero's
        gold value on the website and some kind of visual feedback for the purchase.

    **Alternative JavaScript function call:
    -<button data-py-function="consume" data="{{ item.id }}"
        onClick="remove(this)"></button>
    -Where onClick is a local function to run. "this" is the button object itself.


    NOTES:
        1. The data attribute can be used to send more complex data.
        2. The onClick function could be called by the XHTTP script at the bottom of static/layout.html
            it could then respond to changes in the database. It may need to.
        3. data-* can be anything for any specific values. Might be needed in the
            future for expansions.
    """

    @staticmethod
    def buy(hero, database, arg_dict):
        """Allow the user to buy items from the Blacksmith.
        Returns an error if the character doesn't have enough gold.
        """
        item_id = arg_dict.get('data', None, type=int)
        location = arg_dict.get('location', None, type=str)
        item = database.create_item(item_id)
        if hero.gold >= item.buy_price:
            hero.inventory.add_item(item)
            hero.gold -= item.buy_price
            # return buy success event.
            # Test event later against posible quest events conditions.
            # for path in hero.quest_paths:
            #     if (path.active and
            #         path.quest.name == "Get Acquainted with the Blacksmith" and
            #         path.stage == 2 and
            #         location in ["/store/armoury", "/store/weaponry"]):
            #         path.advance()
            engine = Engine(database)
            engine.spawn(
                'buy_event',
                hero,
                description="{} buys a/an {}.".format(hero.name, item.name)
            )

            return "{}: id={}&&{}".format(item.name, item.id, hero.gold)
        return "error: not enough gold!"

    @staticmethod
    def consume(hero, database, arg_dict):
        """Apply the effect of a potion when the hero consumes it.
        NOTE: the item is then deleted from the hero's inventory and the database.
        """
        item_id = arg_dict.get('data', None, type=int)
        item = database.get_item_by_id(item_id)
        item.apply_effect(hero)
        database.delete_item(item_id)
        return "success"

    @staticmethod
    def equip(hero, database, arg_dict):
        item_id = arg_dict.get('data', None, type=int)
        item = database.get_item_by_id(item_id)
        ids_to_unequip = hero.inventory.equip(item)
        hero.refresh_character()
        engine = Engine(database)
        engine.spawn(
            'equip_event',
            hero,
            description="{} equips a/an {}.".format(hero.name, item.name)
        )
        return item.type + "&&" + str(ids_to_unequip)

    @staticmethod
    def unequip(hero, database, arg_dict):
        item_id = arg_dict.get('data', None, type=int)
        item = database.get_item_by_id(item_id)
        hero.inventory.unequip(item)
        hero.refresh_character()
        engine = Engine(database)
        engine.spawn(
            'unequip_event',
            hero,
            description="{} unequips a/an {}.".format(hero.name, item.name)
        )
        return item.type

    def update_ability(hero, database, arg_dict):
        # Format of data in html button is: data = "{{ ability.id }}, {{ ability.tree }}"
        data = arg_dict.get('data', "").split(", ")
        if data:
            ability_id = int(data[0])
            ability_tree = data[1]
        else:
            ability_id = None
            ability_tree = None
            return "error: button came back with an empty string for data"
        print(ability_tree)
        if ability_tree == "basic":
            if hero.basic_ability_points == 0:
                return "error: not enough points, should have been grayed out"
            hero.basic_ability_points -= 1
        elif ability_tree == "archetype":
            if hero.archetype_ability_points == 0:
                return "error: not enough points, should have been grayed out"
            hero.archetype_ability_points -= 1
        ability = database.get_ability_by_id(ability_id)
        if ability.is_max_level():
            return "error: this ability should have been grayed out as it's at max level"
        print("running learn_ability command:" + ability.name)
        ability.level += 1
        new_description = ability.get_description()
        status = ""
        hero.refresh_character()
        if ability.is_max_level():
            status = "max level"
        return "{}&&{}&&{}&&{}&&{}".format(ability_id, ability.level, status, ability_tree, new_description)

    def become_archetype(hero, database, arg_dict):
        archetype = arg_dict.get('data', None, type=str)
        hero.archetype = archetype
        for ability in hero.abilities:
            if ability.tree == "archetype":
                if ability.tree_type != hero.archetype.lower():
                    ability.hidden = True
                    ability.level = 0
                else:
                    ability.hidden = False
                    ability.learnable = True
        return "success"

    def cast_spell(hero, database, arg_dict):
        ability_id = arg_dict.get('data', None, type=int)
        ability = database.get_ability_by_id(ability_id)
        ability.cast(hero)
        return "success"

    @staticmethod
    def update_proficiency(hero, database, arg_dict):
        """Raise proficiency level, decrement proficiency_points.

        Return status of: success, hide_all, hide_this.
        "succes" means hide none ... maybe I should call it that instead?
        """

        tooltip_template = """{{ proficiency.description }}:
{%- set proficiency_tooltip = proficiency.tooltip.split(';') %}
{%- for tooltip in proficiency_tooltip %}
<br>&bull; {{ tooltip }}
{%- endfor %}
<div id="error-{{ proficiency.id }}" style="display:
{%- if proficiency.is_max_level() %} inline{% else %} none
{%- endif %}"><br>{{ proficiency.error }}</div>"""

        id = arg_dict.get('data', None, type=int)
        proficiency = database.get_proficiency_by_id(id)


        # Defensive coding: command buttons should be hidden by JavaScript
        # when no longer valid due to the return values of this function.
        # If for some reason they are still clickable return error to JS console.
        if hero.proficiency_points <= 0 or proficiency.is_max_level():
            return "error: no proficiency_points or proficiency is at max level."

        hero.proficiency_points -= 1
        proficiency.level_up()
        proficiency.update(hero)

        tooltip = render_template_string(tooltip_template,
            proficiency=proficiency, hero=hero)

        if hero.proficiency_points == 0:
            return "hide_all&&{}".format(tooltip)
        elif proficiency.is_max_level():
            return "hide_this&&{}".format(tooltip)
        return "success&&{}".format(tooltip)

    @staticmethod
    def get_message_content_by_id(hero, database, arg_dict):
        """Return the content of a message based on its id."""
        id = arg_dict.get('data', None, type=int)
        message = database.get_object_by_id("Message", id)
        print("Sending message content back to JS.")
        return "{}".format(message.content)

    @staticmethod
    def cmd_functions(name):
        """Use to refer to return a function from string of its name.
        
        Getattr wrapper ...
        """
        return getattr(Command, name)
