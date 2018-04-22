#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

""" These functions control each battle within the game """

from random import randint
from game import round_number_intelligently

def determine_attacker(active, inactive, frozen_counter, combat_log):
    """
    Your chance of attacking should be adding the two fighters' speeds together and seeing what % of that is yours.
    """
    if frozen_counter[active.name] and not frozen_counter[inactive.name]:
        combat_log.append(active.name + " is frozen! " + inactive.name + " automatically gets to attack.")
        return inactive, active,combat_log
    if frozen_counter[inactive.name] and not frozen_counter[active.name]:
        combat_log.append(inactive.name + " is frozen! " + active.name + " automatically gets to attack.")
        return active, inactive,combat_log
    if frozen_counter[inactive.name] and frozen_counter[active.name]:
        combat_log.append("Both players are frozen. Not sure how to code it so I just ignore it >.<")
    random = randint(1,int((active.get_summed_proficiencies('speed').final + inactive.get_summed_proficiencies('speed').final)*100))
    if active.get_summed_proficiencies('speed').final*100 > random:
        return active,inactive,combat_log
    else:
        return inactive, active,combat_log

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

def determine_life_steal(attacker, base_damage):
    static_amount = int(attacker.get_summed_proficiencies('lifesteal_static').final)
    percent_amount = round_number_intelligently((attacker.get_summed_proficiencies('lifesteal_percent').final / 100) * base_damage)
    return static_amount + percent_amount

def apply_poison(attacker, defender, counter, combat_log):
    random = randint(1, 100)
    if (attacker.get_summed_proficiencies('poison_chance').final > random) and (attacker.get_summed_proficiencies('poison_amount').final > 0):
        counter[defender.name] = attacker.get_summed_proficiencies('poison_duration').final
        combat_log.append(attacker.name + " has applied a poison! It will last " + str(int(counter[defender.name])) + " more rounds.")
    return counter,combat_log

def calculate_poison_damage(inflictor, receiver):
    poison = int(inflictor.get_summed_proficiencies('poison_amount').final)
    poison *= (1 - int(receiver.get_summed_proficiencies('resist_poison').final))
    return poison

def apply_freezing(attacker, defender, combat_log, frozen_counter):
    random = randint(1, 100)
    if attacker.get_summed_proficiencies('freezing_chance').final > random:
        combat_log.append(defender.name + " was frozen!")
        frozen_counter[defender.name] = True
    return combat_log, frozen_counter

# BUG: Lifesteal lets you go beyond maximum HP. Also let's enemy drop below 0. Easy fix!

def battle_logic(active_player, inactive_player):
    """ Runs the entire battle simulator """
    # Currently just takes 1 away from health of whoever attacks slower each round. Ends when someone dies.
    combat_log = ["At the start of the battle: " + active_player.name + " Health: " + str(active_player.base_proficiencies['health'].current) + "  " + inactive_player.name + " Health: " + str(inactive_player.base_proficiencies['health'].current)]
    poison_counter = {active_player.name: 0, inactive_player.name: 0}
    frozen_counter = {active_player.name: False, inactive_player.name: False}
    while active_player.base_proficiencies['health'].current > 0 and inactive_player.base_proficiencies['health'].current > 0:
        for combatant in poison_counter:
            if combatant == active_player.name:
                receiever = active_player
                inflictor = inactive_player
            else:
                receiever = inactive_player
                inflictor = active_player
            if poison_counter[combatant] > 0:
                poison_counter[combatant] -= 1
                poison = calculate_poison_damage(inflictor, receiever)
                receiever.base_proficiencies['health'].current -= poison
                combat_log.append(receiever.name + " takes " + str(poison) + " poison damage!")
        for combatant in frozen_counter:
            if active_player.name == combatant:
                combatant = active_player
            elif inactive_player.name == combatant:
                combatant = inactive_player
            if frozen_counter[combatant.name] and randint(1,100) > combatant.get_summed_proficiencies('thawing_chance').final:
                combat_log.append(combatant.name + " thaws out! They may attack as normal.")
                frozen_counter[combatant.name] = False
        attacker,defender,combat_log = determine_attacker(active_player, inactive_player, frozen_counter, combat_log)
        combat_log.append(attacker.name + " is attacking.")
        if determine_if_hits(attacker, defender): # If there is a hit, you need to check for lifesteal, applying poison, etc.
            base_damage = calculate_damage(attacker, defender)
            if determine_if_critical_hit(attacker):
                combat_log.append(attacker.name + " lands a critical hit!")
                base_damage = add_killshot_multiplier(attacker, base_damage)
            else:
                combat_log.append(attacker.name + " hits.")
            lifesteal = determine_life_steal(attacker, base_damage)
            if lifesteal:
                defender.base_proficiencies['health'].current -= lifesteal
                attacker.base_proficiencies['health'].current += lifesteal
                if attacker.base_proficiencies['health'].current > attacker.get_summed_proficiencies('health').final:
                    attacker.base_proficiencies['health'].current = attacker.get_summed_proficiencies('health').final
                combat_log.append(attacker.name + " steals " + str(lifesteal) + " life! He now has " + str(attacker.base_proficiencies['health'].current) + " life remaining.")
            poison_counter,combat_log = apply_poison(attacker, defender, poison_counter, combat_log)
            combat_log,frozen_counter = apply_freezing(attacker, defender, combat_log, frozen_counter)
            defender.base_proficiencies['health'].current -= base_damage
            combat_log.append(defender.name + " takes " + str(base_damage) + ". He has " + str(defender.base_proficiencies['health'].current) + " health remaining.")
        else:
            combat_log.append(attacker.name + " misses.")

    active_player.base_proficiencies['health'].current = max(active_player.base_proficiencies['health'].current, 0)
    inactive_player.base_proficiencies['health'].current = max(inactive_player.base_proficiencies['health'].current, 0)
    return combat_log
