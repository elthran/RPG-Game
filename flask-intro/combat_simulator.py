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

def determine_attacker_defender(character1 ,character2):
    character1_chance = (0.5 + (character1.attack_speed - character2.attack_speed) / 2) * 100
    if character1_chance >= random.randint(0,100):
        return character1, character2
    return character2, character1

def determine_attack_success(attacker, defender):   # Need to check for each type of possible miss separately.
    if attacker.attack_accuracy < random.randint(0,35):
        return False
    return True

def determine_damage(attacker, defender):   # Need raw damage, then separate functions for reducing damage.
    attack_damage = random.randint(attacker.minimum_damage, attacker.maximum_damage)
    attack_damage = attack_damage * (1 - defender.defence_modifier / 100)
    attack_damage = math.floor(attack_damage)
    return attack_damage

def battle_logic(character1 ,character2):
    print(character1.name + " Health: " + str(character1.current_health) + "\n" + character2.name + " Health: " + str(character2.current_health) + "\n")
    while character1.current_health > 0 and character2.current_health > 0:
        attacker,defender = determine_attacker_defender(character1, character2)
        if determine_attack_success(attacker, defender):
            print("                           " + attacker.name + " has HIT!!!!!!")
            defender.current_health -= determine_damage(attacker, defender)
        else:
            print(attacker.name + " misses " + defender.name)
        print(attacker.name + " Health: " + str(attacker.current_health) + "\n" + defender.name + " Health: " + str(defender.current_health) + "\n\n")
    if character1.current_health <= 0:
        print(character1.name + " is dead")
    else:
        print(character2.name + " is dead")

monster = monster_generator(7)
battle_hero = Hero()
battle_hero.update_secondary_attributes()
battle_hero.refresh_character()
print(monster)
print("\nName: " + battle_hero.name,"\nDamage: " + str(battle_hero.minimum_damage) + "-" + str(battle_hero.maximum_damage), "\nHealth: " + str(battle_hero.current_health) + "/" + str(battle_hero.max_health), "\nAttack Speed: " + str(battle_hero.attack_speed), "\nAccuracy: " + str(battle_hero.attack_accuracy) + "\n")
battle_logic(battle_hero, monster)
