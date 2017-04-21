class Proficiency(object):
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.level = 0
        self.value = value
        self.next_value = False
