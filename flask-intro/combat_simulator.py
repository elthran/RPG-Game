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

# gives a list of distribution of the chance to strike a certain number of times
def determine_attacker(character1 ,character2, last_attacker):
    if last_attacker and last_attacker.name == character1.name:
        return character2
    else:
        return character1

def determine_attack_success(attacker, defender):
    if attacker.attack_accuracy < random.randint(0,35):
        return False
    return True

def determine_damage(attacker, defender):
    attack_damage = random.randint(attacker.minimum_damage, attacker.maximum_damage)
    attack_damage = attack_damage * (1 - defender.defence_modifier / 100)
    return attack_damage


def battle_logic(character1 ,character2):
    print(character1.name + " Health: " + str(character1.current_health) + "\n" + character2.name + " Health: " + str(character2.current_health) + "\n")
    #combat_log = []
    #combat_log.append(("Enemy HP:", str(enemy.current_health) + "/" + str(enemy.max_health)))
    #combat_log.append(("Hero HP:", str(myHero.current_health) + "/" + str(myHero.max_health)))
    current_attacker = None
    while character1.current_health > 0 and character2.current_health > 0:
        if determine_attacker(character1, character2, current_attacker) == character1:
            current_attacker = character1
            if determine_attack_success(character1, character2):
                print("                           " + character1.name + " has HIT!!!!!!")
                character2.current_health -= determine_damage(character1, character2)
            else:
                print(character1.name + " misses " + character2.name)
        elif determine_attacker(character1 ,character2, current_attacker) == character2:
            current_attacker = character2
            if determine_attack_success(character2, character1):
                print("                           " + character2.name + " has HIT!!!!!!")
                character1.current_health -= determine_damage(character2, character1)
            else:
                print(character2.name + " misses " + character1.name)
        else:
            print("Can't determine attacker")
        print(character1.name + " Health: " + str(character1.current_health) + "\n" + character2.name + " Health: " + str(character2.current_health) + "\n\n")
    if character1.current_health <= 0:
        print(character1.name + " is dead")
    else:
        print(character2.name + " is dead")

monster = monster_generator(10)
battle_hero = Hero()
battle_hero.update_secondary_attributes()
battle_hero.refresh_character()
print(monster)
battle_logic(battle_hero, monster)
