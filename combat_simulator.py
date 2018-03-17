#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

""" These functions control each battle within the game """

from random import randint
from game import round_number_intelligently

def determine_attacker(active, inactive):
    random = randint(1,int((active.get_summed_proficiencies('speed').final + inactive.get_summed_proficiencies('speed').final)*100))
    if active.get_summed_proficiencies('speed').final*100 > random:
        return active,inactive
    else:
        return inactive, active

def determine_if_hits(attacker, defender):
    random = randint(1,100)
    attackers_chance = 75 + attacker.get_summed_proficiencies('accuracy').final - defender.get_summed_proficiencies('evade').final
    if attackers_chance >= random:
        return True
    return False

def determine_if_critical_hit(attacker):
    random = randint(1,100)
    if attacker.get_summed_proficiencies('precision').final >= random:
        return True
    return False

def calculate_damage(attacker, defender):
    average_damage = attacker.get_summed_proficiencies('damage').final * attacker.get_summed_proficiencies('combat').final / 100
    damage = average_damage * (1 - defender.get_summed_proficiencies('defence').final)
    damage = max(round_number_intelligently(damage),1)
    return damage

def add_killshot_multiplier(attacker, damage):
    return (damage * attacker.get_summed_proficiencies('killshot').final)

def determine_life_steal(attacker):
    return attacker.get_summed_proficiencies('lifesteal').final


"""
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
    # Currently just takes 1 away from health of whoever attacks slower each round. Ends when someone dies.
    combat_log = ["At the start of the battle: " + active_player.name + " Health: " + str(active_player.base_proficiencies['health'].current) + "  " + inactive_player.name + " Health: " + str(inactive_player.base_proficiencies['health'].current)]
    while active_player.base_proficiencies['health'].current > 0 and inactive_player.base_proficiencies['health'].current > 0:
        attacker,defender = determine_attacker(active_player,inactive_player)
        combat_log.append(attacker.name + " is attacking.")
        if determine_if_hits(attacker, defender):
            if determine_if_critical_hit(attacker):
                combat_log.append(attacker.name + " lands a critical hit!")
                damage = add_killshot_multiplier(attacker, calculate_damage(attacker, defender))
            else:
                combat_log.append(attacker.name + " hits.")
                damage = calculate_damage(attacker, defender)
            defender.base_proficiencies['health'].current -= damage
            combat_log.append(defender.name + " takes " + str(damage) + ". He has " + str(defender.base_proficiencies['health'].current) + " health remaining.")
            #lifesteal = determine_life_steal(attacker)
            #if lifesteal > 0:
            #    attacker.base_proficiencies['health'].current += lifesteal
            #    combat_log.append(attacker.name + " steals " + str(lifesteal) + " life!")
        else:
            combat_log.append(attacker.name + " misses.")

    active_player.base_proficiencies['health'].current = max(active_player.base_proficiencies['health'].current, 0)
    inactive_player.base_proficiencies['health'].current = max(inactive_player.base_proficiencies['health'].current, 0)
    return combat_log
