import pdb

class Command:
    """Run a list of html update commands based on the string cmd.
    
    Usage:
    in app.py
    
    from commands import Command
    
    @app.route('/<cmd>')
    def command(cmd=None):
        try:
            response = Command.cmd_functions[cmd](myHero, database=database, arg_dict=request.args)
            database.update()
            # pdb.set_trace()
            return response
        except KeyError as ex:
            print("Warning: invalid key {}".format(ex))
            print("Valid keys are: {}".format(list(Command.cmd_functions.keys())))
            # Look in the not yet refractored list of if statemens ...
        
    This should call the function and execute it as defined in the cmd_functions dict.
    
    The format for a button is:
    <button class="command" data="{{ item.id }}" onClick="toggleEquip(this)">Equip</button>
    
    Explained:
        class="command" -> causes this button to call the command code above.
        data=... -> sends unique data to the python program that can be used to whatever you want.
        onClick=... -> a local JS function that modifies the info on this end.
        Equip -> a.k.a. the "innerHTML" -> this is the actual command sent to @app.route('/<cmd>')
            it picks what function is executed by the python server.
            
    NOTES:
        the data attribute can be used to send more complex data.
        the onClick function could be called by the XHTTP script at the bottom of static/layout.html
            it could then respond to changes in the database. It may need to.
    """
    
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
        
        Current argument parsing looks like:
        #JinJa2
        <button class="command  command-{{ item.buy_name }}" 
            value="buy?item_name={{ item.name }}">Buy</button>
        #HTML
        <button class="command  command-Medium Helmet_buy" value="buy?item_name=Medium Helmet">
        #Python arg parsing
        my_arg = arg_dict.get('item_name', None, type=str)
        Where 'buy' calls this function a.k.a. <cmd>. item_name is the keyword
        and "Medium Helmet" is the variable.
        """
        # BUY FROM BLACKSMITH
        
        item_id = arg_dict.get('data', None, type=int)
        # pdb.set_trace()
        
        item = database.create_item(item_id)
        if hero.gold >= item.buy_price:
            hero.inventory.add_item(item)
            hero.gold -= item.buy_price 
            #return buy success event.
            #Test event later against posible quest events conditions.
            for path in hero.quest_paths:
                if path.active and path.quest.name == "Get Acquainted with the Blacksmith" and \
                    path.stage == 2:
                    path.advance()
            return "success", 200, {'Content-Type': 'text/plain'}  
        return "success", 200, {'Content-Type': 'text/plain'}
        
    def consume(hero, database, arg_dict):
        """Apply the effect of a potion when the hero consumes it.
        
        NOTE: the item is then deleted from the hero's inventory and the database.
        """
        item_id = arg_dict.get('data', None, type=int)
        item = database.get_item_by_id(item_id)
        
        item.apply_effect(hero)
        database.delete_item(item_id)
        return "success", 200, {'Content-Type': 'text/plain'}
    
    def equip(hero, database, arg_dict):
        item_id = arg_dict.get('data', None, type=int)
        item = database.get_item_by_id(item_id)
        
        hero.inventory.equip(item)
        
    def unequip(hero, database, arg_dict):
        item_id = arg_dict.get('data', None, type=int)
        item = database.get_item_by_id(item_id)
        
        hero.inventory.unequip(item)

        
    cmd_functions = {
        'buy': buy,
        'choose_religion': choose_religion,
        "consume": consume,
        "equip": equip,
        "unequip": unequip,
    }
