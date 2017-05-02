#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

"""All secondary functions are determined in this file. They follow the same pattern:
    - Set up the ratio of attributes
    - Scale the attribute
    - (Optional) Round the decimal place if needed
    That way you can easily either adjust the ratio or you can adjust the scaling!

    y = -(10c / (ax + 10)) + c  => the smaller a is, the slower it reaches the cap, c
    y = a sin(cx) + bx  => where b is slope, a is steepness, and c is frequency

    """

import math

def update_minimum_damage(myHero):
    """ Minimum amount of damage you can do when hitting an opponent """
    minimum_damage = (5 * myHero.attributes.strength.level) + (1 * myHero.attributes.agility.level)
    minimum_damage = 0.1 * math.sin(minimum_damage) + 0.2 * minimum_damage
    minimum_damage = math.floor(minimum_damage)
    return minimum_damage

def update_maximum_damage(myHero):
    """ Maximum amount of damage you can do when hitting an opponent """
    maximum_damage = (1 * myHero.attributes.strength.level) + (4 * myHero.attributes.agility.level)
    maximum_damage = 0.2 * math.sin(maximum_damage) + 0.3 * maximum_damage + update_minimum_damage(myHero)
    maximum_damage = math.floor(maximum_damage)
    return maximum_damage

def update_attack_speed(myHero):
    """ Not sure yet. """
    attack_speed = (7 * myHero.attributes.agility.level) + (2 * myHero.attributes.reflexes.level)
    attack_speed = - (10 / (attack_speed * 0.006 + 10)) + 1
    attack_speed = round(attack_speed, 2)
    return attack_speed

def update_attack_accuracy(myHero):
    """ Chance of successfully hitting an enemy in combat """
    attack_accuracy = (8 * myHero.attributes.agility.level) + (3 * myHero.attributes.reflexes.level) + (1 * myHero.attributes.perception.level)
    attack_accuracy = - (500 / (attack_accuracy * 0.08 + 10)) + 50
    attack_accuracy = math.floor(attack_accuracy)
    return attack_accuracy

def update_first_strike_chance(myHero):
    """ Not sure yet. """
    first_strike_chance = (5 * myHero.attributes.agility.level) + (2 * myHero.attributes.reflexes.level)
    first_strike_chance = - (300 / (first_strike_chance * 0.07 + 10)) + 30
    first_strike_chance = math.floor(first_strike_chance)
    return first_strike_chance

def update_critical_hit_chance(myHero):
    """ Chance of hitting the enemy in a critical location, causing bonus damage """
    critical_hit_chance = (7 * myHero.attributes.agility.level) + (2 * myHero.attributes.perception.level)
    critical_hit_chance = - (300 / (critical_hit_chance * 0.07 + 10)) + 30
    critical_hit_chance = math.floor(critical_hit_chance)
    return critical_hit_chance

def update_critical_hit_modifier(myHero):
    """ How much extra damage you do when you critical hit """
    critical_hit_modifier = (1 * update_maximum_damage(myHero)) + (5 * myHero.attributes.agility.level)
    critical_hit_modifier = 0.05 * math.sin(critical_hit_modifier) + 0.007 * critical_hit_modifier + 1
    critical_hit_modifier = round(critical_hit_modifier, 1)
    return critical_hit_modifier

def update_defence_modifier(myHero):
    """ The % of damage reduced when hit """
    defence_modifier = (6 * myHero.attributes.resilience.level)
    defence_modifier = - (350 / (defence_modifier * 0.09 + 10)) + 35
    defence_modifier = math.floor(defence_modifier)
    return defence_modifier

def update_evade_chance(myHero):
    """ Chance to dodge an attack in combat """
    evade_chance = (5 * myHero.attributes.reflexes.level) + (2 * myHero.attributes.perception.level)
    evade_chance = - (250 / (evade_chance * 0.08 + 10)) + 25
    evade_chance = math.floor(evade_chance)
    return evade_chance

def update_parry_chance(myHero):
    """ Chance to parry when fighting with a weapon """
    parry_chance = (5 * myHero.attributes.reflexes.level) + (1 * myHero.attributes.agility.level) + (3 * myHero.attributes.perception.level)
    parry_chance = - (400 / (parry_chance * 0.1 + 10)) + 40
    parry_chance = math.floor(parry_chance)
    return parry_chance

def update_riposte_chance(myHero):
    """ Chance of counter attacking after a successful parry """
    riposte_chance = (5 * myHero.attributes.agility.level) + (3 * myHero.attributes.perception.level) + (1 * myHero.attributes.reflexes.level)
    riposte_chance = - (400 / (riposte_chance * 0.1 + 10)) + 40
    riposte_chance = math.floor(riposte_chance)
    return riposte_chance

def update_block_chance(myHero):
    """ Chance to blck when using a shield """
    block_chance = (5 * myHero.attributes.reflexes.level) + (3 * myHero.attributes.agility.level) + (2 * myHero.attributes.strength.level)
    block_chance = - (400 / (block_chance * 0.08 + 10)) + 40
    block_chance = math.floor(block_chance)
    return block_chance

def update_block_reduction(myHero):
    """ Percent of damage reduced when you successfully block """
    block_reduction = (2 * myHero.attributes.strength.level) + (2 * myHero.attributes.resilience.level)
    block_reduction = - (400 / (block_reduction * 0.08 + 10)) + 40
    block_reduction = math.floor(block_reduction)
    return block_reduction

def update_stealth_skill(myHero):
    """ Chance of being undetected """
    stealth_skill = (5 * myHero.attributes.reflexes.level) + (3 * myHero.attributes.perception.level) + (2 * myHero.attributes.agility.level)
    stealth_skill = - (250 / (stealth_skill * 0.05 + 10)) + 25
    stealth_skill = math.floor(stealth_skill)
    return stealth_skill

def update_faith(myHero):
    """ Spell Power/Damage """
    faith = (5 * myHero.attributes.divinity.level) + (1 * myHero.attributes.wisdom.level)
    faith = 0.1 * math.sin(faith) + 0.2 * faith
    faith = math.floor(faith)
    return faith

def update_bartering(myHero):
    """ A modifier to the price you pay at stores """
    bartering = (9 * myHero.attributes.charisma.level) + (1 * myHero.attributes.wisdom.level)
    bartering = - (250 / (bartering * 0.05 + 10)) + 25
    bartering = math.floor(bartering)
    return bartering

def update_oration(myHero):
    """ Determines success rate of dialogue as well as which dialogue options are open to you """
    oration = (5 * myHero.attributes.charisma.level) + (3 * myHero.attributes.wisdom.level)
    oration = - (250 / (oration * 0.05 + 10)) + 25
    oration = math.floor(oration)
    return oration

def update_knowledge(myHero):
    """ Determines how much your character knows about the world """
    knowledge = (10 * myHero.attributes.wisdom.level) + (1 * myHero.attributes.perception.level)
    knowledge = 0.1 * math.sin(knowledge) + 0.2 * knowledge
    knowledge = math.floor(knowledge)
    return knowledge

def update_luck_chance(myHero):
    """ This can be applied to almost anything in the game. Chance for a really lucky outcome """
    luck_chance = (5 * myHero.attributes.fortuity.level)
    luck_chance = - (50 / (luck_chance * 0.01 + 10)) + 5
    luck_chance = math.floor(luck_chance)
    return luck_chance

def update_sanctity_maximum(myHero):
    """ Basically your mana. Required to cast spells and use abilities. Should slowly recover over time. """
    sanctity_maximum = (5 * myHero.attributes.divinity.level) + (1 * myHero.attributes.wisdom.level) + 3
    sanctity_maximum = 0.1 * math.sin(sanctity_maximum) + 0.2 * sanctity_maximum
    sanctity_maximum = math.floor(sanctity_maximum)
    return sanctity_maximum

def update_health_maximum(myHero):
    """ How much health your Hero has. At zero, you die. """
    maximum_health = (10 * myHero.attributes.vitality.level) + (2 * myHero.attributes.resilience.level) + (1 * myHero.attributes.strength.level) + 10
    maximum_health = 0.1 * math.sin(maximum_health) + 0.25 * maximum_health
    maximum_health = math.floor(maximum_health)
    return maximum_health

def update_endurance_maximum(myHero):
    """ How many actions you can perform, such as moving on the map or fighting. It slowly recovers over time. """
    endurance_maximum = (5 * myHero.attributes.fortitude.level) + (1 * myHero.attributes.resilience.level) + (1 * myHero.attributes.strength.level) + 25
    endurance_maximum = 0.1 * math.sin(endurance_maximum) + 0.05 * endurance_maximum + 4
    endurance_maximum = math.floor(endurance_maximum)
    return endurance_maximum

def update_storage_maximum(myHero):
    """ How much you can carry in your inventory + items equipped. """
    storage_maximum = (5 * myHero.attributes.strength.level) + (4 * myHero.attributes.resilience.level)
    storage_maximum = 0.1 * math.sin(storage_maximum) + 0.08 * storage_maximum
    storage_maximum = math.floor(storage_maximum)
    return storage_maximum





# BELOW HERE ARE THE MONSTER SECONDARY ATTRIBUTES

def update_monster_minimum_damage(monster):
    """ Minimum amount of damage you can do when hitting an opponent """
    minimum_damage = (5 * monster.primary_attributes["Strength"]) + (1 * monster.primary_attributes["Agility"])
    minimum_damage = 0.02 * math.sin(minimum_damage) + 0.1 * minimum_damage
    minimum_damage = math.floor(minimum_damage)
    return minimum_damage

def update_monster_maximum_damage(monster):
    """ Maximum amount of damage you can do when hitting an opponent """
    maximum_damage = (1 * monster.primary_attributes["Strength"]) + (4 * monster.primary_attributes["Agility"])
    maximum_damage = 0.05 * math.sin(maximum_damage) + 0.125 * maximum_damage + update_monster_minimum_damage(monster)
    maximum_damage = math.floor(maximum_damage)
    return maximum_damage

def update_monster_attack_speed(monster):
    """ Not sure yet. """
    attack_speed = (7 * monster.primary_attributes["Agility"]) + (2 * monster.primary_attributes["Reflexes"])
    attack_speed = - (10 / (attack_speed * 0.006 + 10)) + 1
    attack_speed = round(attack_speed, 2)
    return attack_speed

def update_monster_attack_accuracy(monster):
    """ Chance of successfully hitting an enemy in combat """
    attack_accuracy = (8 * monster.primary_attributes["Agility"]) + (3 * monster.primary_attributes["Reflexes"]) + (1 * monster.primary_attributes["Perception"])
    attack_accuracy = - (500 / (attack_accuracy * 0.05 + 10)) + 50
    attack_accuracy = math.floor(attack_accuracy)
    return attack_accuracy

def update_monster_first_strike_chance(monster):
    """ Not sure yet. """
    first_strike_chance = (5 * monster.primary_attributes["Agility"]) + (2 * monster.primary_attributes["Reflexes"])
    first_strike_chance = - (300 / (first_strike_chance * 0.07 + 10)) + 30
    first_strike_chance = math.floor(first_strike_chance)
    return first_strike_chance

def update_monster_critical_hit_chance(monster):
    """ Chance of hitting the enemy in a critical location, causing bonus damage """
    critical_hit_chance = (7 * monster.primary_attributes["Agility"]) + (2 * monster.primary_attributes["Perception"])
    critical_hit_chance = - (300 / (critical_hit_chance * 0.07 + 10)) + 30
    critical_hit_chance = math.floor(critical_hit_chance)
    return critical_hit_chance

def update_monster_critical_hit_modifier(monster):
    """ How much extra damage you do when you critical hit """
    critical_hit_modifier = (1 * update_monster_maximum_damage(monster)) + (5 * monster.primary_attributes["Agility"])
    critical_hit_modifier = 0.05 * math.sin(critical_hit_modifier) + 0.007 * critical_hit_modifier + 1
    critical_hit_modifier = round(critical_hit_modifier, 1)
    return critical_hit_modifier

def update_monster_defence_modifier(monster):
    """ The % of damage reduced when hit """
    defence_modifier = (6 * monster.primary_attributes["Resilience"])
    defence_modifier = - (350 / (defence_modifier * 0.09 + 10)) + 35
    defence_modifier = math.floor(defence_modifier)
    return defence_modifier

def update_monster_evade_chance(monster):
    """ Chance to dodge an attack in combat """
    evade_chance = (5 * monster.primary_attributes["Reflexes"]) + (2 * monster.primary_attributes["Perception"])
    evade_chance = - (250 / (evade_chance * 0.08 + 10)) + 25
    evade_chance = math.floor(evade_chance)
    return evade_chance

def update_monster_parry_chance(monster):
    """ Chance to parry when fighting with a weapon """
    parry_chance = (5 * monster.primary_attributes["Reflexes"]) + (1 * monster.primary_attributes["Agility"]) + (3 * monster.primary_attributes["Perception"])
    parry_chance = - (400 / (parry_chance * 0.1 + 10)) + 40
    parry_chance = math.floor(parry_chance)
    return parry_chance

def update_monster_riposte_chance(monster):
    """ Chance of counter attacking after a successful parry """
    riposte_chance = (5 * monster.primary_attributes["Agility"]) + (3 * monster.primary_attributes["Perception"]) + (1 * monster.primary_attributes["Reflexes"])
    riposte_chance = - (400 / (riposte_chance * 0.1 + 10)) + 40
    riposte_chance = math.floor(riposte_chance)
    return riposte_chance

def update_monster_block_chance(monster):
    """ Chance to blck when using a shield """
    block_chance = (5 * monster.primary_attributes["Reflexes"]) + (3 * monster.primary_attributes["Agility"]) + (2 * monster.primary_attributes["Strength"])
    block_chance = - (400 / (block_chance * 0.08 + 10)) + 40
    block_chance = math.floor(block_chance)
    return block_chance

def update_monster_block_reduction(monster):
    """ Percent of damage reduced when you successfully block """
    block_reduction = (2 * monster.primary_attributes["Strength"]) + (2 * monster.primary_attributes["Resilience"])
    block_reduction = block_reduction ** 0.75
    block_reduction = math.floor(block_reduction)
    return block_reduction

def update_monster_stealth_skill(monster):
    """ Chance of being undetected """
    stealth_skill = (5 * monster.primary_attributes["Reflexes"]) + (3 * monster.primary_attributes["Perception"]) + (2 * monster.primary_attributes["Agility"])
    stealth_skill = - (250 / (stealth_skill * 0.05 + 10)) + 25
    stealth_skill = math.floor(stealth_skill)
    return stealth_skill

def update_monster_faith(monster):
    """ Spell Power/Damage """
    faith = (5 * monster.primary_attributes["Divinity"]) + (1 * monster.primary_attributes["Wisdom"])
    faith = (0.2 * faith) ** 0.9
    faith = math.floor(faith)
    return faith

def update_monster_luck_chance(monster):
    """ This can be applied to almost anything in the game. Chance for a really lucky outcome """
    luck_chance = (5 * monster.primary_attributes["Fortuity"])
    luck_chance = - (50 / (luck_chance * 0.01 + 10)) + 5
    luck_chance = math.floor(luck_chance)
    return luck_chance

def update_monster_sanctity_maximum(monster):
    """ Basically your mana. Required to cast spells and use abilities. Should slowly recover over time. """
    sanctity_maximum = (5 * monster.primary_attributes["Divinity"]) + (1 * monster.primary_attributes["Wisdom"]) + 3
    sanctity_maximum = (0.8 * sanctity_maximum) ** 0.9
    sanctity_maximum = math.floor(sanctity_maximum)
    return sanctity_maximum

def update_monster_health_maximum(monster):
    """ How much health your Hero has. At zero, you die. """
    health_maximum = (10 * monster.primary_attributes["Vitality"]) + (2 * monster.primary_attributes["Resilience"]) + (1 * monster.primary_attributes["Strength"]) + 10
    health_maximum = 0.1 * math.sin(health_maximum) + 0.1 * health_maximum
    health_maximum = math.floor(health_maximum)
    return health_maximum

