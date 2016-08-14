from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *
from bestiary import *
import math, random

def battle_logic(myHero,enemy):
    enemy.hp = 1 + myHero.level
    while myHero.current_hp > 0 and enemy.hp > 0:
        myHero.current_hp -= math.floor(enemy.damage-2)
        enemy.hp -= math.floor(myHero.damage * random.randint(1,2))
        if myHero.current_hp < 0:
            myHero.current_hp = 0
        if enemy.hp < 0:
            enemy.hp = 0
    return myHero.current_hp,enemy.hp
