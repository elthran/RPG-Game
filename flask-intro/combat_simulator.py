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
    """ The first character returned is the attacker. The second character returned is the defender. """ 
    character1_chance = 50 + ((character1.attack_speed - character2.attack_speed) * 100)
    if character1_chance >= random.randint(0, 100):
        return character1, character2
    return character2, character1

def determine_attack_success(attacker, defender):
    """ Determines if the hit is successful or not """
    print("\n" + attacker.name + " is attempting to attack " + defender.name)
    if attacker.attack_accuracy < random.randint(0,10):
        print(attacker.name + " misses " + defender.name)
        return False
    if defender.evade_chance >= random.randint(0,20):
        print(defender.name + " has dodged the attack!")
        return False
    if defender.parry_chance >= random.randint(0,20):
        print(defender.name + " has parried the attack!")
        return False
    print("                           " + attacker.name + " has HIT!!!!!!")
    return True

def determine_block_success(defender):
    """ Determines if the hit is blocked or not """
    if defender.block_chance >= random.randint(0,20):
        print(defender.name + " has blocked the attack!")
        return True
    return False

def determine_raw_damage(attacker):
    """ Determines how much damage the attacker will hit for """
    raw_attack_damage = random.randint(attacker.minimum_damage, attacker.maximum_damage)
    raw_attack_damage = round(raw_attack_damage, 3)
    print(attacker.name + " hits for " + str(raw_attack_damage) + " damage.")
    return raw_attack_damage

def determine_modified_damage(defender, raw_damage):
    """ Determines how much damage the defender will actually take after defence bonuses """
    modified_attack_damage = raw_damage * (1 - defender.defence_modifier / 100)
    modified_attack_damage = round(modified_attack_damage, 3)
    print(defender.name + " loses " + str(modified_attack_damage) + " health.")
    return modified_attack_damage

def battle_logic(character1 ,character2):
    """ Runs the entire battle simulator """
    print(character1.name + " Health: " + str(character1.current_health) + "\n" + character2.name + " Health: " + str(character2.current_health) + "\n")
    while character1.current_health > 0 and character2.current_health > 0:
        attacker,defender = determine_attacker_defender(character1, character2)
        if determine_attack_success(attacker, defender):
            raw_attack_damage = determine_raw_damage(attacker)
            if determine_block_success(defender):
                raw_attack_damage = raw_attack_damage * (100 - defender.block_reduction) / 100
            modified_attack_damage = determine_modified_damage(defender, raw_attack_damage)
            modified_attack_damage = int(round(modified_attack_damage))
            defender.current_health -= modified_attack_damage   
            print(attacker.name + " Health: " + str(attacker.current_health) + "\n" + defender.name + " Health: " + str(defender.current_health))
    if character1.current_health <= 0:
        print(character1.name + " is dead")
    else:
        print(character2.name + " is dead")



""" Test functions below. Not needed for the final product """
monster = monster_generator(7)
battle_hero = Hero()
battle_hero.update_secondary_attributes()
battle_hero.refresh_character()
print(monster)
print("\nName: " + battle_hero.name,"\nDamage: " + str(battle_hero.minimum_damage) + "-" + str(battle_hero.maximum_damage), "\nHealth: " + str(battle_hero.current_health) + "/" + str(battle_hero.max_health), "\nAttack Speed: " + str(battle_hero.attack_speed), "\nAccuracy: " + str(battle_hero.attack_accuracy) + "\n")
battle_logic(battle_hero, monster)
