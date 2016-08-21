from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *
from bestiary import *
import math, random

def battle_logic(myHero,enemy):
    combat_log = []
    combat_log.append(("Enemy:", "I start with " + str(enemy.current_hp) + " health."))
    combat_log.append(("Hero:", "I start with " + str(myHero.current_hp) + " health."))
    
    while myHero.current_hp > 0 and enemy.current_hp > 0:
        # Calculate how many attacks every gets this round (for now it's just 1, but the faster you are this should increase)
        enemy_attacks = 1
        myHero_attacks = 1
        # Perform attacks
        while (enemy_attacks + myHero_attacks) > 0:
            # Enemy attacks first
            if myHero.dodge_chance > random.randint(0,100):
                combat_log.append(("Hero:", "I have dodged your attack."))
            elif enemy.accuracy < random.randint(0,100):
                combat_log.append(("Enemy:", "I have swung and missed an attack."))
            else:
                enemy_damage = math.floor((random.randint(enemy.min_damage, enemy.max_damage)) * ((100 - myHero.defence_modifier) / 100)) # Calculate enemy's damage
                enemy_damage = 0 # JIMMY ADDED THIS
                combat_log.append(("Enemy:", "I hit you for " + str(enemy_damage) + " damage."))
                myHero.current_hp -= enemy_damage
                if myHero.current_hp <= 0:
                    combat_log.append(("Hero:", "I have been killed."))
                    break
                combat_log.append(("Hero:", "I have " + str(myHero.current_hp) + " health remaining."))
            # Hero attacks next
            if enemy.dodge_chance > random.randint(0,100):
                combat_log.append(("Enemy:", "I have dodged your attack."))
            elif myHero.attack_accuracy < random.randint(0,100):
                combat_log.append(("Hero:", "I have swung and missed an attack."))
            else:
                myHero_damage = math.floor((random.randint(myHero.min_damage, myHero.max_damage)) * ((100 - enemy.defence_modifier) / 100)) # Calculate hero's damage
                myHero_damage = 10 # JIMMY ADDED THIS
                combat_log.append(("Hero:", "I hit the enemy for " + str(myHero_damage) + " damage."))
                enemy.current_hp -= myHero_damage
                if enemy.current_hp <= 0:
                    combat_log.append(("Enemy:", "I have been killed."))
                    break
                combat_log.append(("Enemy:", "I have " + str(enemy.current_hp) + " health remaining."))

            myHero_attacks -= 1
            enemy_attacks -= 1

    return myHero.current_hp,enemy.current_hp,combat_log
