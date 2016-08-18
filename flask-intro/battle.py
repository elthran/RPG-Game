from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *
from bestiary import *
import math, random

def battle_logic(myHero,enemy):
    enemy.hp = 5 + myHero.level
    while myHero.current_hp > 0 and enemy.hp > 0:
        enemy_damage = random.randint(enemy.min_damage, enemy.max_damage) * enemy.speed
        myHero.current_hp -= math.floor(enemy_damage / myHero.defence)
        enemy.hp -= math.floor(random.randint(myHero.min_damage, myHero.max_damage) * myHero.speed)
        if myHero.current_hp < 0:
            myHero.current_hp = 0
        if enemy.hp < 0:
            enemy.hp = 0
    return myHero.current_hp,enemy.hp
