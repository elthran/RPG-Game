#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

""" These functions control each battle within the game """

from random import randint

def determine_attacker(active, inactive):
    speed_sum = active.get_summed_proficiencies('speed').final + inactive.get_summed_proficiencies('speed').final
    random = randint(0,speed_sum)
    print(active.get_summed_proficiencies('speed').final,inactive.get_summed_proficiencies('speed').final,random)
    if active.get_summed_proficiencies('speed').final >= randint(0,speed_sum):
        return active,inactive
    else:
        return inactive, active

"""
def determine_if_hits(accuracy):
    print ("Chance for attacker to hit their opponent is: " + str(accuracy) + "%")
    if randint(0,100) <= accuracy:
        return True
    return False

def determine_if_critical_hit(chance):
    print ("Chance for critical hit is: " + str(chance) + "%")
    if randint(0,100) < chance:
        return True
    return False

def calculate_damage(minimum, maximum):
    if maximum <= minimum:
        maximum = minimum + 1 # This avoids a bug with randint looking at impossible ranges
    damage = randint(minimum, maximum)
    print ("Unmodified attack will hit for this much damage: " + str(damage))
    return damage

def critical_hit_modifier(original_damage, modifier):
    print ("Critical hit! Damage multiplied by: " + str(modifier))
    damage = original_damage * modifier
    return damage

def determine_evade(chance):
    print ("Chance to evade is: " + str(chance) + "%")
    if randint(0,100) < chance:
        return True
    return False

def determine_block_chance(chance):
    print ("Chance to block is: " + str(chance) + "%")
    if randint(0,100) < chance:
        return True
    return False

def determine_block_amount(original_damage, modifier):
    print ("You will block this percent of damage: " + str(modifier) + "%")
    damage = original_damage * (1 - modifier)
    if damage < 1:
        damage = 1
    return damage

def determine_parry_chance(chance):
    print ("Chance to parry is: " + str(chance) + "%")
    if randint(0,100) < chance:
        return True
    return False

def determine_riposte_chance(chance):
    print ("Chance to riposte is: " + str(chance) + "%")
    if randint(0,100) < chance:
        return True
    return False

def lower_fatigue(fatigue):
    fatigue -= 1
    if fatigue < 0:
        fatigue = 0
    return fatigue
"""

def battle_logic(active_player, inactive_player):
    """ Runs the entire battle simulator """
    count = 5
    combat_log = active_player.name + " Health: " + str(active_player.get_summed_proficiencies('health').current) + "  " + inactive_player.name + " Health: " + str(inactive_player.get_summed_proficiencies('health').current)
    while active_player.base_proficiencies['health'].current >=0 and inactive_player.base_proficiencies['health'].current >= 0 and count >= 0:
        attacker,defender = determine_attacker(active_player,inactive_player)
        print("Before attack:",attacker.base_proficiencies['health'].current,defender.base_proficiencies['health'].current)
        count-= 1
        defender.base_proficiencies['health'].current -= 1
        print("After attack:", attacker.base_proficiencies['health'].current,defender.base_proficiencies['health'].current)
    return combat_log
