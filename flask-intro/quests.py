class Quest(object):
    def __init__(self, name, myHero, stages=1, stage_descriptions=["Unknown"], reward_xp=0):
        self.name = name
        self.myHero = myHero
        self.stages = stages
        self.stage_descriptions = stage_descriptions
        self.current_stage = 0
        self.display_stage = 1
        self.reward_xp = reward_xp
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
            self.myHero.completed_quests.append(self)
            self.completed = True
        else:
            self.update_quest_stage()

class Primary_Quest(Quest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

