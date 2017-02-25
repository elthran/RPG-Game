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
    if attacker.attack_accuracy < random.randint(0,25):
        return (attacker.name + " misses " + defender.name)
    if defender.evade_chance >= random.randint(0,25):
        return (defender.name + " has dodged an attack!")
    if defender.parry_chance >= random.randint(0,25):
        return (defender.name + " has parried an attack!")
    return True

def determine_block_success(defender):
    """ Determines if the hit is blocked or not """
    if defender.block_chance >= random.randint(0,50):
        return True
    return False

def determine_critical_hit_success(attacker):
    """ Determines if the hit is a critical hit or not. Can only happen if it's not blocked by the defender. """
    if attacker.critical_hit_chance >= random.randint(0,10):
        return True
    return False

def determine_raw_damage(attacker):
    """ Determines how much damage the attacker will hit for """
    raw_attack_damage = random.randint(attacker.minimum_damage, attacker.maximum_damage)
    raw_attack_damage = round(raw_attack_damage, 3)
    return raw_attack_damage

def determine_raw_critical_hit_damage(attacker):
    """ Determines the modifier for adjusting how much damage the attacker hits for """
    critical_hit_modifier = attacker.critical_hit_modifier + (random.randint(0,10) / 20)
    critical_hit_modifier = round(critical_hit_modifier, 2)
    return critical_hit_modifier

def determine_modified_damage(defender, raw_damage):
    """ Determines how much damage the defender will actually take after defensive bonuses """
    modified_attack_damage = raw_damage * (1 - defender.defence_modifier / 100)
    modified_attack_damage = round(modified_attack_damage, 3)
    return modified_attack_damage

def battle_logic(character1 ,character2):
    """ Runs the entire battle simulator """
    combat_log = [(character1.name + " Health: " + str(character1.current_health)), (character2.name + " Health: " + str(character2.current_health))]
    battle_results = ""
    while character1.current_health > 0 and character2.current_health > 0:
        attacker,defender = determine_attacker_defender(character1, character2)
        attack_success = determine_attack_success(attacker, defender)
        if attack_success == True:
            raw_attack_damage = determine_raw_damage(attacker)
            if determine_block_success(defender):
                raw_attack_damage = raw_attack_damage * (100 - defender.block_reduction) / 100
                combat_log.append(defender.name + " has blocked the attack!")
            elif determine_critical_hit_success(attacker):
                critical_hit_modifier = determine_raw_critical_hit_damage(attacker)
                raw_attack_damage *= critical_hit_modifier
                combat_log.append(attacker.name + " has critically hit, getting a " + str(critical_hit_modifier) + " damage modifier!!")
            modified_attack_damage = determine_modified_damage(defender, raw_attack_damage)
            modified_attack_damage = int(round(modified_attack_damage))
            defender.current_health -= modified_attack_damage
            combat_log.append(attacker.name + " hits for " + str(modified_attack_damage) + " damage. " + defender.name + " now has " + str(defender.current_health) + " health.")   
        else:
            combat_log.append(attack_success)
    if character1.current_health <= 0:
        battle_results += (character1.name + " is dead")
    else:
        battle_results += (character2.name + " is dead")
    return character1.current_health,character2.current_health,combat_log,battle_results



""" Test functions below. Not needed for the final product
monster = monster_generator(7)
battle_hero = Hero()
battle_hero.update_secondary_attributes()
battle_hero.refresh_character()
print(monster)
print("\nName: " + battle_hero.name,"\nDamage: " + str(battle_hero.minimum_damage) + "-" + str(battle_hero.maximum_damage), "\nHealth: " + str(battle_hero.current_health) + "/" + str(battle_hero.max_health), "\nAttack Speed: " + str(battle_hero.attack_speed), "\nAccuracy: " + str(battle_hero.attack_accuracy) + "\n")
battle_logic(battle_hero, monster)
"""
