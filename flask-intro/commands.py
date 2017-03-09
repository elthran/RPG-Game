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

        
    cmd_functions = {
        'forgoth': forgoth_update_hero_religion,
        'dryarch': dryarch_update_hero_religion
    }
