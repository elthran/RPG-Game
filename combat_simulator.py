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

def determine_life_steal(attacker, base_damage):
    static_amount = int(attacker.get_summed_proficiencies('lifesteal_static').final)
    percent_amount = round_number_intelligently((attacker.get_summed_proficiencies('lifesteal_percent').final / 100) * base_damage)
    return static_amount + percent_amount

def apply_poison(attacker, defender, counter, combat_log):
    random = randint(1, 100)
    if (attacker.get_summed_proficiencies('poison_chance').final > random) and (attacker.get_summed_proficiencies('poison_amount').final > 0):
        counter[defender.name] = attacker.get_summed_proficiencies('poison_duration').final
        combat_log.append(attacker.name + " has applied a poison! It will last" + str(counter[defender.name]) + " more rounds.")
    return counter,combat_log

def calculate_poison_damage(inflictor, receiver):
    poison = int(inflictor.get_summed_proficiencies('poison_amount').final)
    poison *= (1 - int(receiver.get_summed_proficiencies('resist_poison').final))
    return poison

# BUG: Lifesteal lets you go beyond maximum HP. Also let's enemy drop below 0. Easy fix!

def battle_logic(active_player, inactive_player):
    """ Runs the entire battle simulator """
    # Currently just takes 1 away from health of whoever attacks slower each round. Ends when someone dies.
    combat_log = ["At the start of the battle: " + active_player.name + " Health: " + str(active_player.base_proficiencies['health'].current) + "  " + inactive_player.name + " Health: " + str(inactive_player.base_proficiencies['health'].current)]
    poison_counter = {active_player.name: 0, inactive_player.name: 0}
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
        print(poison_counter) # TEMP
        attacker,defender = determine_attacker(active_player,inactive_player)
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
            defender.base_proficiencies['health'].current -= base_damage
            combat_log.append(defender.name + " takes " + str(base_damage) + ". He has " + str(defender.base_proficiencies['health'].current) + " health remaining.")
        else:
            combat_log.append(attacker.name + " misses.")

    active_player.base_proficiencies['health'].current = max(active_player.base_proficiencies['health'].current, 0)
    inactive_player.base_proficiencies['health'].current = max(inactive_player.base_proficiencies['health'].current, 0)
    return combat_log
