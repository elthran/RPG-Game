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
    """
    Your chance of attacking should be adding the two fighters' speeds together and seeing what % of that is yours.
    """
    random = randint(1,int((active.get_summed_proficiencies('speed').final + inactive.get_summed_proficiencies('speed').final)*100))
    if active.get_summed_proficiencies('speed').final*100 > random:
        return active,inactive
    else:
        return inactive, active

def determine_if_hits(attacker, defender):
    """
    By default, you have a 75% chance of hitting. This can be modified by your accuracy and their evasion.
    """
    random = randint(1,100)
    attackers_chance = 75 + attacker.get_summed_proficiencies('accuracy').final - defender.get_summed_proficiencies('evade').final
    if attackers_chance >= random:
        return True
    return False

def calculate_damage(attacker, defender):
    damage = (attacker.get_summed_proficiencies('damage').final + attacker.get_summed_proficiencies('combat').final) / 2
    damage = damage * (1 - defender.get_summed_proficiencies('defence').final)
    damage = max(round_number_intelligently(damage),1)
    return damage

def determine_if_critical_hit(attacker):
    random = randint(1,100)
    if attacker.get_summed_proficiencies('precision').final >= random:
        return True
    return False

def add_killshot_multiplier(attacker, damage):
    return (damage * attacker.get_summed_proficiencies('killshot').final)

def determine_life_steal(attacker):
    amount = int(attacker.get_summed_proficiencies('lifesteal').final)
    return amount


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
# BUG: Lifesteal lets you go beyond maximum HP. Also let's enemy drop below 0. Easy fix!

def battle_logic(active_player, inactive_player):
    """ Runs the entire battle simulator """
    # Currently just takes 1 away from health of whoever attacks slower each round. Ends when someone dies.
    combat_log = ["At the start of the battle: " + active_player.name + " Health: " + str(active_player.base_proficiencies['health'].current) + "  " + inactive_player.name + " Health: " + str(inactive_player.base_proficiencies['health'].current)]
    while active_player.base_proficiencies['health'].current > 0 and inactive_player.base_proficiencies['health'].current > 0:
        attacker,defender = determine_attacker(active_player,inactive_player)
        combat_log.append(attacker.name + " is attacking.")
        if determine_if_hits(attacker, defender):
            base_damage = calculate_damage(attacker, defender)
            if determine_if_critical_hit(attacker):
                combat_log.append(attacker.name + " lands a critical hit!")
                damage = add_killshot_multiplier(attacker, base_damage)
            else:
                combat_log.append(attacker.name + " hits.")
            lifesteal = determine_life_steal(attacker)
            if lifesteal:
                defender.base_proficiencies['health'].current -= lifesteal
                attacker.base_proficiencies['health'].current += lifesteal
                combat_log.append(attacker.name + " steals " + str(lifesteal) + " life! He now has " + str(attacker.base_proficiencies['health'].current) + " life remaining.")
            defender.base_proficiencies['health'].current -= base_damage
            combat_log.append(defender.name + " takes " + str(base_damage) + ". He has " + str(defender.base_proficiencies['health'].current) + " health remaining.")
            #lifesteal = determine_life_steal(attacker)
            #if lifesteal > 0:
            #    attacker.base_proficiencies['health'].current += lifesteal
            #    combat_log.append(attacker.name + " steals " + str(lifesteal) + " life!")
        else:
            combat_log.append(attacker.name + " misses.")

    active_player.base_proficiencies['health'].current = max(active_player.base_proficiencies['health'].current, 0)
    inactive_player.base_proficiencies['health'].current = max(inactive_player.base_proficiencies['health'].current, 0)
    return combat_log
