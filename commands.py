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
            response = Command.cmd_functions(cmd)(hero, database=database, arg_dict=request.args)
            database.update()
            return response
        except KeyError as ex:
            print("Warning: invalid key {}".format(ex))
            # Look in the not yet refactored list of if statements ...
        
    This should call the function and execute it in the Command class.
    
    The format for a button is:
    Format
    -<button class="command" name="consume" data="{{ item.id }}" data-function="functionName"></button>
    -<button class="command" name="consume" data="{{ item.id }}" onClick="remove(this)"></button>
    -Where class="command" means this object runs command code.
    -Where data is the items database id. Or any other data necessary.
    -Where name="consume" is the name of the Python method/function to run (in commands.py).
    -Where data-function="functionName" is the name of a JavaScript function that accepts
        data as a return value from the Python function defined in name="".
        NOTE: This function runs after the python code returns a response.
        "onClick" does not. It runs first/or independantly?
    -Where onClick is a local function to run. "this" is the button object itself.
    
            
    NOTES:
        the data attribute can be used to send more complex data.
        the onClick function could be called by the XHTTP script at the bottom of static/layout.html
            it could then respond to changes in the database. It may need to.
    """
    
    
    #Marked for update!
    #Uses obsolete code.
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
        
    def consume(hero, database, arg_dict):
        """Apply the effect of a potion when the hero consumes it.
        
        NOTE: the item is then deleted from the hero's inventory and the database.
        """
        item_id = arg_dict.get('data', None, type=int)
        item = database.get_item_by_id(item_id)
        
        item.apply_effect(hero)
        database.delete_item(item_id)
        return "success"
    
    def equip(hero, database, arg_dict):
        item_id = arg_dict.get('data', None, type=int)
        item = database.get_item_by_id(item_id)
        ids_to_unequip = hero.inventory.equip(item)

        hero.refresh_character()
        
        return item.type + "&&" + str(ids_to_unequip)
        
    def unequip(hero, database, arg_dict):
        item_id = arg_dict.get('data', None, type=int)
        item = database.get_item_by_id(item_id)

        hero.refresh_character()
        
        hero.inventory.unequip(item)
        return item.type

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


    def cmd_functions(name):
        """Use to refer to return a function from string of its name.
        
        Getattr wrapper ...
        """
        return getattr(Command, name)

