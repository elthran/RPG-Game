import pdb

from flask import render_template_string


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
    Format (3 different ways ... from most flexible and longest to type to
        least flexible and shortest to type)
    -<button class="command" data-name="consume" data="{{ item.id }}" data-function="javascript_consume"></button>
    -<button class="command" name="consume" data="{{ item.id }}" data-function="javascript_consume"></button>
    -<button class="command" data="{{ item.id }}" data-function="javascript_consume"">Consume</button>
    -Where class="command" means this object runs command code.
    -Where data is the python object's database id. Or any other data necessary.
    -Where data-name="consume" is the name of the Python method/function to run (in commands.py).
        -Or name="consume" or 'innerHTML' >Consume< (minus ><) this is from older code
    -Where data-function="javascript_consume" is the name of a JavaScript function that accepts
        data as a return value from the Python function defined in name="".
        NOTE: This function runs after the python code returns a response.
        "onClick" does not. It runs first/or independantly?

    Usage:
        Use the python functions if you need to change the database or hero
        object.
        Use the JS functions if you need to update the website data.
            e.g. buy and item ... send it to the python code with the item's id
        Drop hero's gold ... add item to inventory.
        Then send back the confirmation to the JS function and update the hero's
        gold value on the website and some kind of visual feedback for the purchase.

    **Alternative JavaScript function call:
    -<button class="command" data-name="consume" data="{{ item.id }}" onClick="remove(this)"></button>
    -Where onClick is a local function to run. "this" is the button object itself.


    NOTES:
        1. The data attribute can be used to send more complex data.
        2. The onClick function could be called by the XHTTP script at the bottom of static/layout.html
            it could then respond to changes in the database. It may need to.
        3. data-* can be anything for any specific values. Might be needed in the
            future for expansions.
    """


    #Marked for update!
    #Uses obsolete code.
    @staticmethod
    def choose_religion(hero, database, arg_dict):
        # pdb.set_trace()
        button_name = arg_dict.get('innerHTML', None, type=str)
        #Update value in database.
        #Swap value for religion between Forgoth and Dryarch.
        hero.religion = "Dryarch" if button_name == "Dryarch" else "Forgoth"


        #Return a string to be parsed by the xhttp code.
        #Replace all occurrences of html with id equal to old value with new value.
        #This updates the value and the id!
        """
        <span id="hero_religion">{{ myHero.religion }}</span>
        This will update the value of myHero.religion if it is inside the above span tag.
        """
        return "{id}={value}".format(id='hero_religion', value=hero.religion)

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
            #return buy success event.
            #Test event later against posible quest events conditions.
            for path in hero.quest_paths:
                if (path.active and
                    path.quest.name == "Get Acquainted with the Blacksmith" and
                    path.stage == 2 and
                    location in ["/store/armoury", "/store/weaponry"]):
                    path.advance()
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

        return item.type + "&&" + str(ids_to_unequip)

    @staticmethod
    def unequip(hero, database, arg_dict):
        item_id = arg_dict.get('data', None, type=int)
        item = database.get_item_by_id(item_id)

        hero.refresh_character()

        hero.inventory.unequip(item)
        return item.type

    def update_ability(hero, database, arg_dict):
        if hero.basic_ability_points == 0:
            return "error: not enough points, should have been grayed out"
        ability_id = arg_dict.get('data', None, type=int)
        ability = database.get_ability_by_id(ability_id)
        if ability.is_max_level():
            return "error: this ability should have been grayed out as it's at max level"
        print("running learn_ability command:" + ability.name)
        ability.level += 1
        hero.basic_ability_points -= 1
        status = ""
        if ability.is_max_level():
            status = "max level"
        return "{}&&{}&&{}".format(ability.level, hero.basic_ability_points, status)

    def cast_spell(hero, database, arg_dict):
        ability_id = arg_dict.get('data', None, type=int)
        ability = database.get_ability_by_id(ability_id)
        ability.cast(hero)
        return "success"

    @staticmethod
    def level_proficiency(hero, database, arg_dict):
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
{%- if proficiency.is_max_level(hero) %} inline{% else %} none
{%- endif %}"><br>{{ proficiency.error }}</div>"""

        id = arg_dict.get('data', None, type=int)
        proficiency = database.get_proficiency_by_id(id)

        # Defensive coding: command buttons should be hidden by JavaScript
        # when no longer valid due to the return values of this function.
        # If for some reason they are still clickable return error to JS console.
        if hero.proficiency_points <= 0 or proficiency.is_max_level(hero):
            return "error: no proficiency_points or proficiency is at max level."

        hero.proficiency_points -= 1
        proficiency.level_up()
        proficiency.update(hero)

        tooltip = render_template_string(tooltip_template,
            proficiency=proficiency, hero=hero)

        if hero.proficiency_points == 0:
            return "hide_all&&{}".format(tooltip)
        elif proficiency.is_max_level(hero):
            return "hide_this&&{}".format(tooltip)
        return "success&&{}".format(tooltip)

    @staticmethod
    def upgrade_ability(hero, database, arg_dict):
        """Update the Ability object located at id.

        This function returns the relevant display data to some JS code.

        Maybe this also needs to be able to "add" an Ability to the Hero object?
        if the Ability is at level 0? Or would the Hero have all Abilities
        but not display them if they are level 0?
        """
        ability_id = arg_dict.get('data', None, type=int)
        ability = database.get_object_by_id("Ability", ability_id)

        # This is a dummy function that will update the abilities level
        # and various display properties ... and the hero object it pertains
        # to.
        ability.update_level()

        # The return is a dummy function ... it would need to send all
        # the data to make the JS/HTML display correctly.
        return "update_ability_display&&{}".format(ability.display_name)

    @staticmethod
    def cmd_functions(name):
        """Use to refer to return a function from string of its name.
        
        Getattr wrapper ...
        """
        return getattr(Command, name)
