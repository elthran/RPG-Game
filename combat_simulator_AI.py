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
import math, random

def battle_logic(hero ,monster):
    """ Runs the entire battle simulator """
    combat_log = [(hero.name + " Health: " + str(hero.health)), (monster.name + " Health: " + str(monster.health))]
    battle_results = ""
    while hero.health > 0 and hero.health > 0:
        hero.health -= monster.proficiencies.attack_damage.value
        monster.health -= hero.proficiencies.attack_damage.value
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
