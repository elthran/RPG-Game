#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

""" this is called if you fight. it runs the battle simulator """



from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *
from bestiary import *
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
    if maximum < minimum:
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

def battle_logic(hero, monster):
    """ Runs the entire battle simulator """
    combat_log = [hero.name + " Health: " + str(hero.health) + "  " + monster.name + " Health: " + str(monster.health)]
    battle_results = ""
    print ("Hero health: " + str(hero.health) + "~~~~Monster health: " + str(monster.health))
    while (hero.health > 0) and (monster.health > 0):
        attacker, defender = determine_attacker(hero, monster, hero.proficiencies.attack_speed.speed, monster.proficiencies.attack_speed.speed, hero.proficiencies.first_strike.chance, monster.proficiencies.first_strike.chance)
        print ("ATTACKER IS " + attacker.name)
        if determine_if_hits(attacker.proficiencies.attack_accuracy.accuracy):
            print ("HIT")
            damage = calculate_damage(attacker.proficiencies.attack_damage.minimum, attacker.proficiencies.attack_damage.maximum)
        else:
            combat_log.append(attacker.name + " misses!")
            print ("MISS")
            continue
        if determine_if_critical_hit(attacker.proficiencies.critical_hit.chance):
            damage = critical_hit_modifier(damage, attacker.proficiencies.critical_hit.modifier)
        if determine_evade(defender.proficiencies.evade.chance):
            combat_log.append(str(defender.name) + " evaded!")
            print ("EVADED")
            continue
        if determine_block_chance(defender.proficiencies.block.chance):
            combat_log.append(str(defender.name) + " blocked some damage!")
            print ("BLOCKED")
            damage = determine_block_amount(damage, defender.proficiencies.block.modifier)
        if determine_parry_chance(defender.proficiencies.parry.chance):
            print ("PARRIED")
            continue
        if determine_riposte_chance(defender.proficiencies.riposte.chance):
            print ("RIPOSTED")
            continue
        print ("Final damage is: " + str(damage))
        defender.health -= damage
        print (str(defender.name) + "'s new health is: " + str(defender.health))
        combat_log.append("%s hits for %i. %s has %i health left.\n" % (attacker.name, damage, defender.name, defender.health))
    if hero.health <= 0:
        battle_results += (hero.name + " is dead")
    else:
        battle_results += (monster.name + " is dead")
    return hero.health, monster.health, combat_log, battle_results
