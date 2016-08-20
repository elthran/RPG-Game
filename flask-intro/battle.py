from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *
from bestiary import *
import math, random

def battle_logic(myHero,enemy):
    while myHero.current_hp > 0 and enemy.current_hp > 0:
        # Calculate enemy's damage
        enemy_damage = random.randint(enemy.min_damage, enemy.max_damage) * enemy.speed
        # Calculate how many attacks enemy gets this round (Placeholder)
        enemy_attacks = 1
        # Perform attacks
        while enemy_attacks > 0:
        # Calculate if hero dodges
            if myHero.dodge_chance > random.randint(0,100):
                enemy_attacks -= 1
            elif enemy.accuracy < random.randint(0,100):
                enemy_attacks -= 1
            else:
                myHero.current_hp -= math.floor(enemy_damage / myHero.defence_modifier)
        enemy.current_hp -= math.floor(random.randint(myHero.min_damage, myHero.max_damage) * myHero.attack_speed)
        if myHero.current_hp < 0:
            myHero.current_hp = 0
        if enemy.current_hp < 0:
            enemy.current_hp = 0
    return myHero.current_hp,enemy.current_hp
