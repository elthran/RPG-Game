from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *
from bestiary import *
import math, random

def battle_logic(myHero,enemy):
    print("in battle logic")
    print(myHero.current_hp)
    while myHero.current_hp > 0 and enemy.current_hp > 0:
        print("in battle logic while loop")
        print(myHero.current_hp)
        combat_log = []
        combat_log.append(("Enemy:", "I start with " + str(enemy.current_hp) + " health."))
        combat_log.append(("Hero:", "I start with " + str(myHero.current_hp) + " health."))
        
        # Calculate how many attacks enemy gets this round (Placeholder)
        enemy_attacks = 1        
        # Perform attacks
        while enemy_attacks > 0:
        # Calculate if hero dodges
            if myHero.dodge_chance > random.randint(0,100):
                combat_log.append(("Enemy:", "I have dodged an attack."))
            elif enemy.accuracy < random.randint(0,100):
                combat_log.append(("Enemy:", "I have swung and missed an attack."))
            else:
                enemy_damage = math.floor((random.randint(enemy.min_damage, enemy.max_damage) * enemy.speed * 5) / myHero.defence_modifier) # Calculate enemy's damage
                combat_log.append(("Enemy:", "I hit you for " + str(enemy_damage) + " damage."))
                myHero.current_hp -= enemy_damage
            combat_log.append(("Hero:", "I have " + str(myHero.current_hp) + " health remaining."))
            enemy_attacks -= 1

        hero_attacks = 1
        while hero_attacks > 0:
        # Calculate if hero dodges
            if enemy.dodge_chance > random.randint(0,100):
                combat_log.append(("Hero:", "I have dodged an attack."))
            elif myHero.attack_accuracy < random.randint(0,100):
                combat_log.append(("Hero:", "I have swung and missed an attack."))
            else:
                myHero_damage = math.floor((random.randint(myHero.min_damage, myHero.max_damage) * myHero.attack_speed * 5) / enemy.defence_modifier) # Calculate enemy's damage
                combat_log.append(("Hero:", "I hit the enemy for " + str(myHero_damage) + " damage."))
                enemy.current_hp -= myHero_damage
            combat_log.append(("Enemy:", "I have " + str(enemy.current_hp) + " health remaining."))
            hero_attacks -= 1
            
        if myHero.current_hp <= 0:
            myHero.current_hp = 0
            combat_log.append(("Hero:", "I have been killed."))
        elif enemy.current_hp <= 0:
            enemy.current_hp = 0
            combat_log.append(("Hero:", "I have killed the monster."))
    return myHero.current_hp,enemy.current_hp,combat_log
