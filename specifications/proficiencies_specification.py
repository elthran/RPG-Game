"""
Class Health(Proficiency):
    @property
    def base(self):
        return 5 + self.level  # some function based on level.
        # The actual "value". Your actual health is 5 at lvl 0
        
    @property
    def final_value(self):
        self.base * self.mod
    
    def __init__(self):
        self.level = 0  # Hidden profs don’t need a level. Non-hidden profs default at 0
        self.hidden = False  # This is true for unmodifiable profs
        self.mod = 1  # This is true for all profs so should just be inherited
    

class Hero:
    def update_profs(self):
        for prof in self.base_proficiencies:
            sum_base = self.base
            sum_mod = self.mod
    
            for item in self.equipped_items:
                sum_base += item.profs[prof.name].base
                sum_mod += item.profs[prof.name].mod
    
            For ability in hero.known_abilities:
                sum_base += ability.profs[prof.name].base
                sum_mod += ability.profs[prof.name].mod

            self.summed_profs[prof.name].base = sum_base
            self.summed_profs[prof.name].mod = sum_mod
"""
