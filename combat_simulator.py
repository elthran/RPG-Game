#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

""" These functions control each battle within the game """

from random import randint

def determine_attacker(hero, monster, hero_speed, monster_speed, hero_first_strike, monster_first_strike):
    if randint(0,100) < hero_first_strike:
        print ("Hero strikes first because of FIRST STRIKE!")
        return hero, monster
    elif randint(0,100) < monster_first_strike:
        print ("Monster strikes first because of FIRST STRIKE!")
        return monster, hero
    difference = abs(hero_speed - monster_speed)
    if hero_speed > monster_speed:
        hero_chance = (difference / hero_speed)*100 + randint(-20,20)
    else:
        hero_chance = (1-(difference / monster_speed))*100 + randint(-20,20)
    print ("Chance for HERO to attack this round: " + str(hero_chance) + "%")
    if randint(0,100) < hero_chance:
        return hero, monster
    return monster, hero

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

def battle_logic(active_player, inactive_player):
    """ Runs the entire battle simulator """
    combat_log = [active_player.name + " Health: " + str(active_player.proficiencies.health.current) + "  " + inactive_player.name + " Health: " + str(inactive_player.proficiencies.health.current)]
    while (active_player.proficiencies.health.current > 0) and (inactive_player.proficiencies.health.current > 0):
        attacker, defender = determine_attacker(active_player, inactive_player,
                                                active_player.proficiencies.speed.final,inactive_player.proficiencies.speed.final,
                                                active_player.proficiencies.killshot.final, inactive_player.proficiencies.killshot.final
                                                )
        if determine_if_hits(attacker.proficiencies.accuracy.final):
            damage = calculate_damage(attacker.proficiencies.damage.final, attacker.proficiencies.damage.final)
        else:
            combat_log.append(attacker.name + " misses!")
            continue
        if determine_if_critical_hit(attacker.proficiencies.killshot.final):
            damage = critical_hit_modifier(damage, attacker.proficiencies.killshot.final)
        if determine_evade(defender.proficiencies.evade.final):
            combat_log.append(str(defender.name) + " evaded!")
            continue
        if determine_block_chance(defender.proficiencies.block.final):
            combat_log.append(str(defender.name) + " blocked some damage!")
            damage = determine_block_amount(damage, defender.proficiencies.block.final)
        if determine_parry_chance(defender.proficiencies.parry.final):
            continue
        if determine_riposte_chance(defender.proficiencies.riposte.final):
            defender.proficiencies.fatigue.current = lower_fatigue(defender.proficiencies.fatigue.current)
            continue
        defender.proficiencies.health.current -= damage
        attacker.proficiencies.fatigue.current = lower_fatigue(attacker.proficiencies.fatigue.current)
        combat_log.append("%s hits for %i. %s has %i health left.\n" % (attacker.name, damage, defender.name, defender.proficiencies.health.current))
    if active_player.proficiencies.health.current <= 0:
        active_player.proficiencies.health.current = 0
        combat_log.append(active_player.name + " is dead")
    else:
        inactive_player.proficiencies.health.current = 0
        combat_log.append(inactive_player.name + " is dead.\nYou gain " + str(inactive_player.experience_rewarded) + " experience.")
    return active_player.proficiencies.health.current, inactive_player.proficiencies.health.current, combat_log
