class Proficiencies(Base):
    def __init__(self, hero):
        self.hero = hero
        
        proficiencies = [
            Proficiency("max_damage", "Max damage the hero can do"),
            Proficiency("min_damage", "Min damage the hero can do")
        ]
        for proficiency in proficiencies:
            setattr(self, proficiency.name, Proficiency(name))

class Proficiency(object):
    def __init__(self, name, description, attribute_type):
        self.name = name
        self.description = description
        self.attribute_type = attribute_type
        
        self.level = 1
        self.value = 10
        self.next_value = 15
        self.max_level = 1

    def update_testing(self, myHero):
        self.max_level = myHero.primary_attributes["Vitality"] // 2
        if self.max_level < 1:
            self.max_level = 1
        self.value = (self.level * 5) + 5
        self.next_value = ((self.level + 1) * 5) + 5
