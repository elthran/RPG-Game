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
def get_distribution(atk_s,def_s):
    atk_s = float(atk_s)
    def_s = float(def_s)
    ratio = max(atk_s/def_s,def_s/atk_s)
    cap = int(math.ceil(ratio))
    sub_cap = cap - 1
    ratio_i = ratio - sub_cap
    cap_amount = cap * ratio_i
    distribution = []
    total = (1 + sub_cap)*(sub_cap)/2 + cap_amount
    for i in range(1,cap):
        distribution.append(i*100/total)
    distribution.append(cap_amount*100/total)
    return distribution

def calculate_attacks(attacker,defender):
    attacker_atks = 1
    defender_atks = 1
    distribution = get_distribution(attacker.attack_speed,defender.attack_speed)
    print(distribution)
    random_dec = random.randint(0,101)
    num_atks = 0
    print(random_dec)
    for n in distribution:
        num_atks += 1
        random_dec -= n
        if random_dec <= 0:
            break
    if attacker.attack_speed > defender.attack_speed:
        attacker_atks = num_atks
    else:
        defender_atks = num_atks    

    return attacker_atks,defender_atks

'''
hero1 = create_random_hero()
hero1.attack_speed = 2
hero2 = create_random_hero()
hero2.attack_speed = 50
print(calculate_attacks(hero1,hero2))
'''

def battle_logic(myHero,enemy):
    combat_log = []
    combat_log.append(("Enemy HP:", str(enemy.current_health) + "/" + str(enemy.max_health)))
    combat_log.append(("Hero HP:", str(myHero.current_health) + "/" + str(myHero.max_health)))
    
    while myHero.current_health > 0 and enemy.current_health > 0:
        # Calculate how many attacks every gets this round (for now it's just 1, but the faster you are this should increase)
        myHero_attacks, enemy_attacks = calculate_attacks(myHero,enemy)
        # Perform attacks
        while (enemy_attacks + myHero_attacks) > 0:
            # Enemy attacks first
            if myHero.evade_chance > random.randint(0,100):
                combat_log.append(("Hero:", "I have dodged your attack."))
            elif enemy.accuracy < random.randint(0,100):
                combat_log.append(("Enemy:", "I have swung and missed an attack."))
            else:
                enemy_damage = math.ceil((random.randint(enemy.min_damage, enemy.max_damage)) * ((100 - myHero.defence_modifier) / 100)) # Calculate enemy's damage
                enemy_damage = 2
                combat_log.append(("Enemy", "hits you for " + str(enemy_damage) + " damage."))
                myHero.current_health -= enemy_damage
                if myHero.current_health <= 0:
                    combat_log.append(("Hero:", "I have been killed."))
                    break
                combat_log.append(("Hero HP:", str(myHero.current_health) + "/" + str(myHero.max_health)))
            # Hero attacks next
            if enemy.evade_chance > random.randint(0,100):
                combat_log.append(("Enemy:", "I have dodged your attack."))
            elif myHero.attack_accuracy < random.randint(0,100):
                combat_log.append(("You", "swing and miss."))
            else:
                myHero_damage = math.ceil((random.randint(myHero.min_damage, myHero.max_damage)) * ((100 - enemy.defence_modifier) / 100)) # Calculate hero's damage
                myHero_damage = 2
                combat_log.append(("You", "hit the enemy for " + str(myHero_damage) + " damage."))
                enemy.current_health -= myHero_damage
                if enemy.current_health <= 0:
                    combat_log.append(("Enemy:", "I have been killed."))
                    break
                combat_log.append(("Enemy HP:", str(enemy.current_health) + "/" + str(enemy.max_health)))

            myHero_attacks -= 1
            enemy_attacks -= 1

    return myHero.current_health,enemy.current_health,combat_log
