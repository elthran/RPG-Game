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
        return hero
    elif randint(0,100) < monster_first_strike:
        print ("Monster strikes first because of FIRST STRIKE!")
        return monster
    difference = abs(hero_speed - monster_speed)
    if hero_speed > monster_speed:
        hero_chance = (difference / hero_speed)*100 + randint(-20,20)
    else:
        hero_chance = (1-(difference / monster_speed))*100 + randint(-20,20)
    print ("Chance for HERO to attack this round: " + str(hero_chance) + "%")
    if randint(0,100) < hero_chance:
        return hero
    return monster

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
    combat_log = [(hero.name + " Health: " + str(hero.health)), (monster.name + " Health: " + str(monster.health))]
    battle_results = ""
    print ("Hero health: " + str(hero.health) + "~~~~Monster health: " + str(monster.health))
    while (hero.health > 0) and (monster.health > 0):
        attacker = determine_attacker(hero, monster, hero.proficiencies.attack_speed.speed, monster.attack_speed, hero.proficiencies.first_strike.chance, monster.first_strike)
        if attacker == hero:
            print ("ATTACKER IS HERO")
            if determine_if_hits(hero.proficiencies.attack_accuracy.accuracy):
                print ("HIT")
                hero_damage = calculate_damage(hero.proficiencies.attack_damage.minimum, hero.proficiencies.attack_damage.maximum)
            else:
                combat_log.append("Hero misses!")
                print ("MISS")
                continue
            if determine_if_critical_hit(hero.proficiencies.critical_hit.chance):
                hero_damage = critical_hit_modifier(hero_damage, hero.proficiencies.critical_hit.modifier)
            if determine_evade(monster.evade_chance):
                combat_log.append("Monster evaded!")
                print ("EVADED")
                continue
            if determine_block_chance(monster.block_chance):
                combat_log.append("Monster blocked some damage!")
                print ("BLOCKED")
                hero_damage = determine_block_amount(hero_damage, monster.block_reduction)
            if determine_parry_chance(monster.parry_chance):
                print ("PARRIED")
                continue
            if determine_riposte_chance(monster.riposte_chance):
                print ("RIPOSTED")
                continue
            print ("Final damage is: " + str(hero_damage))
            monster.health -= hero_damage
            print ("Monster's new health is: " + str(monster.health))
            combat_log.append("HERO hits for %i. Monster has %i health left.\n" % (hero_damage, monster.health))
        else:
            print ("ATTACKER IS MONSTER")
            if determine_if_hits(monster.attack_accuracy):
                print ("HIT")
                monster_damage = calculate_damage(monster.minimum_damage, monster.maximum_damage)
            else:
                combat_log.append("Monster misses!")
                print ("MISS")
                continue
            if determine_if_critical_hit(monster.critical_hit_chance):
                monster_damage = critical_hit_modifier(monster_damage, monster.critical_hit_modifier)
            if determine_evade(hero.proficiencies.evade.chance):
                combat_log.append("Hero evaded!")
                print ("EVADED")
                continue
            if determine_block_chance(hero.proficiencies.block.chance):
                combat_log.append("Hero blocked some damage!")
                print ("BLOCKED")
                monster_damage = determine_block_amount(monster_damage, hero.proficiencies.block.modifier)
            if determine_parry_chance(hero.proficiencies.parry.chance):
                print ("PARRIED")
                continue
            if determine_riposte_chance(hero.proficiencies.riposte.chance):
                print ("RIPOSTED")
                continue
            print ("Final damage is: " + str(monster_damage))
            hero.health -= monster_damage
            print ("Hero's new health is: " + str(hero.health))
            combat_log.append("MONSTER hits for %i. Monster has %i health left.\n" % (monster_damage, hero.health))
    if hero.health <= 0:
        battle_results += (hero.name + " is dead")
    else:
        battle_results += (monster.name + " is dead")
    return hero.health, monster.health, combat_log, battle_results
