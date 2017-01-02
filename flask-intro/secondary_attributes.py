#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

"""All secondary functions are determined in this file"""

import math

def update_maximum_damage(myHero):
    """ Maximum amount of damage you can do when hitting an opponent """
    maximum_damage = myHero.primary_attributes["Strength"] + myHero.primary_attributes["Agility"]
    maximum_damage = math.floor(maximum_damage)
    return maximum_damage

def update_minimum_damage(myHero):
    """ Minimum amount of damage you can do when hitting an opponent """
    minimum_damage = 0.4 * myHero.max_damage
    minimum_damage = math.floor(minimum_damage)
    return minimum_damage

def update_attack_speed(myHero):
    """ Not sure yet. """
    attack_speed = 0.2 * myHero.primary_attributes["Agility"] + 0.1 * myHero.primary_attributes["Reflexes"]
    attack_speed = round(attack_speed,2)
    return attack_speed

def update_attack_accuracy(myHero):
    """ Chance of successfully hitting an enemy in combat """
    attack_accuracy = 5 * myHero.primary_attributes["Agility"] + 2 * myHero.primary_attributes["Reflexes"] + 2 * myHero.primary_attributes["Perception"]
    attack_accuracy = round(attack_accuracy,2)
    return attack_accuracy

def update_first_strike_chance(myHero):
    """ Not sure yet. """
    first_strike_chance = 5 * myHero.primary_attributes["Agility"] + 2 * myHero.primary_attributes["Reflexes"]
    first_strike_chance = round(first_strike_chance, 2)
    return first_strike_chance

def update_critical_hit_chance(myHero):
    """ Chance of hitting the enemy in a critical location, causing bonus damage """
    critical_hit_chance = 7 * myHero.primary_attributes["Agility"] + 2 * myHero.primary_attributes["Perception"]
    return critical_hit_chance

def update_critical_hit_modifier(myHero):
    """ How much extra damage you do when you critical hit """
    critical_hit_modifier = 2.2 * myHero.max_damage
    return critical_hit_modifier

def update_defence_modifier(myHero):
    """ The % of damage reduced when hit """
    defence_modifier = 6.5 * myHero.primary_attributes["Resilience"] 
    return defence_modifier

def update_evade_chance(myHero):
    """ Chance to dodge an attack in combat """
    evade_chance = 4.7 * myHero.primary_attributes["Reflexes"] + 1.3 * myHero.primary_attributes["Perception"]
    return evade_chance

def update_parry_chance(myHero):
    """ Chance to parry when fighting with a weapon """
    parry_chance = 3.8 * myHero.primary_attributes["Reflexes"] + 2.1 * myHero.primary_attributes["Agility"]
    return parry_chance

def update_riposte_chance(myHero):
    """ Chance of counter attacking after a successful parry """
    riposte_chance = 2.7 * myHero.primary_attributes["Agility"]
    return riposte_chance

def update_block_chance(myHero):
    """ Chance to blck when using a shield """
    block_chance = 5 * myHero.primary_attributes["Reflexes"] + 3.5 * myHero.primary_attributes["Agility"] + 2 * myHero.primary_attributes["Strength"]
    return block_chance

def update_block_reduction(myHero):
    """ Damage reduced when you successfully block """
    block_reduction = 2 * myHero.primary_attributes["Strength"] + 2 * myHero.primary_attributes["Resilience"]
    return block_reduction

def update_stealth_skill(myHero):
    """ Chance of being undetected """
    stealth_skill = 5 * myHero.primary_attributes["Reflexes"] + 3.5 * myHero.primary_attributes["Perception"] + 2 * myHero.primary_attributes["Agility"]
    return stealth_skill

def update_faith(myHero):
    """ Spell Power/Damage """
    faith = 5 * myHero.primary_attributes["Divinity"] + 1.5 * myHero.primary_attributes["Wisdom"]
    faith = math.floor(faith)
    return faith

def update_bartering(myHero):
    """ A modifier to the price you pay at stores """
    bartering = 2 * myHero.primary_attributes["Charisma"]
    return bartering

def update_oration(myHero):
    """ Determines success rate of dialogue as well as which dialogue options are open to you """
    oration = 5 * myHero.primary_attributes["Charisma"] + 3.5 * myHero.primary_attributes["Wisdom"]
    return oration

def update_luck_chance(myHero):
    """ This can be applied to almost anything in the game. Chance for a really lucky outcome """
    luck_chance = 5 * myHero.primary_attributes["Fortuity"]
    return luck_chance

def update_maximum_sanctity(myHero):
    """ Basically your mana. Required to cast spells and use abilities. Should slowly recover over time. """
    maximum_sanctity = 5 * myHero.primary_attributes["Divinity"]
    return maximum_sanctity

def update_maximum_health(myHero):
    """ How much health your Hero has. At zero, you die. """
    maximum_health = 5 * myHero.primary_attributes["Vitality"]
    return maximum_health

def update_maximum_endurance(myHero):
    """ How many actions you can perform, such as moving on the map or fighting. It slowly recovers over time. """
    maximum_endurance = 5 * myHero.primary_attributes["Fortitude"]
    return maximum_endurance

def update_carrying_capacity(myHero):
    """ How much you can carry in your inventory + items equipped. """
    carrying_capacity = 5 * myHero.primary_attributes["Resilience"] + 4 * myHero.primary_attributes["Strength"]
    return carrying_capacity


    
