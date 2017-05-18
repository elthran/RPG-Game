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

def calculate_damage(minimum, maximum):
    damage = randint(minimum, maximum)
    return damage

def determine_attacker(hero, monster, combat_log):
    monster_speed = 1 # Temprary
    difference = abs(hero.proficiencies.attack_speed.speed - monster_speed)
    if hero.proficiencies.attack_speed.speed > monster_speed:
        hero_chance = (difference / hero.proficiencies.attack_speed.speed)*100 + randint(-20,20)
    else:
        hero_chance = (1-(difference / monster_speed))*100 + randint(-20,20)
    combat_log.append("-----------Chance for hero to hit: " + str(hero_chance))
    if randint(0,100) < hero_chance:
        return hero, combat_log
    return monster, combat_log

def battle_logic(hero, monster):
    """ Runs the entire battle simulator """
    combat_log = [(hero.name + " Health: " + str(hero.health)), (monster.name + " Health: " + str(monster.health))]
    battle_results = ""
    while (hero.health > 0) and (monster.health > 0):
        attacker,combat_log = determine_attacker(hero, monster, combat_log)
        if attacker == hero:
            hero_damage = calculate_damage(hero.proficiencies.attack_damage.minimum, hero.proficiencies.attack_damage.maximum)
            monster.health -= hero_damage
            combat_log.append("HERO hits for %i. Monster has %i health left.\n" % (hero_damage, monster.health))
        else:
            monster_damage = calculate_damage(1,1)
            hero.health -= monster_damage
            combat_log.append("MONSTER hits for %i. Monster has %i health left.\n" % (monster_damage, hero.health))
    if hero.health <= 0:
        battle_results += (hero.name + " is dead")
    else:
        battle_results += (monster.name + " is dead")
    return hero.health, monster.health, combat_log, battle_results



""" Test functions below. Not needed for the final product
monster = monster_generator(7)
battle_hero = Hero()
battle_hero.update_secondary_attributes()
battle_hero.refresh_character()
print(monster)
print("\nName: " + battle_hero.name,"\nDamage: " + str(battle_hero.minimum_damage) + "-" + str(battle_hero.maximum_damage), "\nHealth: " + str(battle_hero.health) + "/" + str(battle_hero.max_health), "\nAttack Speed: " + str(battle_hero.attack_speed), "\nAccuracy: " + str(battle_hero.attack_accuracy) + "\n")
battle_logic(battle_hero, monster)
"""
