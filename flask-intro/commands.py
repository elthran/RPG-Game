import pdb

class Command:
    """Run a list of html update commands based on the string cmd.
    
    Usage:
    from commands import Command
    
    @app.route('/<cmd>')
    def command(cmd=None):
        Command.cmd_funtions[cmd]()
        
    This should call the function and execute it as defined in the cmd_functions dict.
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
        <span id="hero.religion">{{ myHero.religion }}</span>
        This will update the value of myHero.religion if it is inside the above span tag.
        """
        return "{id}={value}".format(id='hero_religion', value=hero.religion)
        
        
    def buy_from_blacksmith(hero, database, arg_dict):
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
        
        item_name = arg_dict.get('item_name', None, type=str)
        # pdb.set_trace()
        
        item = database.create_item(item_name)
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

        
    cmd_functions = {
        'buy': buy_from_blacksmith,
        'choose_religion': choose_religion,
    }
