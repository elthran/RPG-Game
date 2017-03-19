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
    
    def forgoth_update_hero_religion(hero):
        old_religion = hero.religion 
        
        #Update value in database.
        hero.religion = "Forgoth"
        
        #Return a string to be parsed by the xhttp code.
        #Replace all occurrences of html with id equal to old value with new value.
        #This updates the value and the id!
        """
        <span id="{{ myHero.religion }}">{{ myHero.religion }}</span>
        This will change the value of this code back and forth between
        values of myHero.religion
        """
        return "{id}={value}".format(id=old_religion, value=hero.religion)

        
    def dryarch_update_hero_religion(hero):
        old_religion = hero.religion
        hero.religion = "Dryarch"
        return "{id}={value}".format(id=old_religion, value=hero.religion)
        
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
        pdb.set_trace()
        for item in database.get_all_store_items():
            if item_name == item.name and hero.gold >= item.buy_price:
                newItem = item
                newItem.update_owner(hero)
                hero.inventory.append(newItem)
                hero.gold -= item.buy_price
                for path in hero.quest_paths:
                    if path.quest.name == "Get Acquainted with the Blacksmith" and path.stage == 2:
                        path.quest.advance_quest()
                return "success", 200, {'Content-Type': 'text/plain'} #//

        
    cmd_functions = {
        'forgoth': forgoth_update_hero_religion,
        'dryarch': dryarch_update_hero_religion,
        'buy': buy_from_blacksmith,
    }
