from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *
from bestiary import *
import math, random

def battle_logic(myHero,enemy):
    combat_log = []
    combat_log.append(("Enemy HP:", str(enemy.current_hp) + "/" + str(enemy.max_hp)))
    combat_log.append(("Hero HP:", str(myHero.current_hp) + "/" + str(myHero.max_hp)))
    
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
                enemy_damage = math.ceil((random.randint(enemy.min_damage, enemy.max_damage)) * ((100 - myHero.defence_modifier) / 100)) # Calculate enemy's damage
                enemy_damage = 2
                combat_log.append(("Enemy", "hits you for " + str(enemy_damage) + " damage."))
                myHero.current_hp -= enemy_damage
                if myHero.current_hp <= 0:
                    combat_log.append(("Hero:", "I have been killed."))
                    break
                combat_log.append(("Hero HP:", str(myHero.current_hp) + "/" + str(myHero.max_hp)))
            # Hero attacks next
            if enemy.dodge_chance > random.randint(0,100):
                combat_log.append(("Enemy:", "I have dodged your attack."))
            elif myHero.attack_accuracy < random.randint(0,100):
                combat_log.append(("You", "swing and miss."))
            else:
                myHero_damage = math.ceil((random.randint(myHero.min_damage, myHero.max_damage)) * ((100 - enemy.defence_modifier) / 100)) # Calculate hero's damage
                myHero_damage = 2
                combat_log.append(("You", "hit the enemy for " + str(myHero_damage) + " damage."))
                enemy.current_hp -= myHero_damage
                if enemy.current_hp <= 0:
                    combat_log.append(("Enemy:", "I have been killed."))
                    break
                combat_log.append(("Enemy HP:", str(enemy.current_hp) + "/" + str(enemy.max_hp)))

            myHero_attacks -= 1
            enemy_attacks -= 1

    return myHero.current_hp,enemy.current_hp,combat_log
