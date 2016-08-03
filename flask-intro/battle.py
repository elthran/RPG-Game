from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *
import math, random

def battle_logic():
    enemy.hp = 10 + myHero.wins
    while myHero.hp > 0 and enemy.hp > 0:
        myHero.hp -= math.floor(enemy.damage * random.randint(1,2))
        enemy.hp -= math.floor(myHero.damage * random.randint(1,2))
        if myHero.hp < 0:
            myHero.hp = 0
        if enemy.hp < 0:
            enemy.hp = 0
    return myHero.hp,enemy.hp
