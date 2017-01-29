from game import *

class Quest(object):
    def __init__(self, name, myHero, stages=1, stage_descriptions=["Unknown"], reward_xp=3):
        self.name = name
        self.myHero = myHero
        self.stages = stages
        self.stage_descriptions = stage_descriptions
        self.current_stage = 0
        self.display_stage = 1
        self.reward_xp = reward_xp
        self.current_description = stage_descriptions[0]
        self.completed = False

    def update_owner(self, myHero):
        self.myHero = myHero

    def update_quest_stage(self):
        if self.current_stage < self.stages: 
            self.current_description = self.stage_descriptions[self.current_stage]

    def advance_quest(self):
        print("my stage:",self.current_stage)
        self.current_stage += 1
        self.display_stage = self.current_stage + 1
        if self.current_stage == self.stages:
            self.myHero.current_exp += self.reward_xp
            self.completed = True
            self.myHero.quest_notification = [self.name, self.reward_xp]
        else:
            self.update_quest_stage()

class Primary_Quest(Quest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


testing_quests = [Quest("Get Acquainted with the Blacksmith", myHero, stages=2, stage_descriptions=["Go talk to the blacksmith.", "Buy your first item."], reward_xp=7), Quest("Equipping/Unequipping", myHero, stages=2, stage_descriptions=["Equip any item.", "Unequip any item."])]
