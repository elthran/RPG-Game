from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *
from bestiary import *
import math, random

def battle_logic():
    game.enemy.hp = 10 + myHero.wins
    while myHero.hp > 0 and game.enemy.hp > 0:
        myHero.hp -= math.floor(game.enemy.damage * random.randint(1,2))
        game.enemy.hp -= math.floor(myHero.damage * random.randint(1,2))
        if myHero.hp < 0:
            myHero.hp = 0
        if game.enemy.hp < 0:
            game.enemy.hp = 0
    return myHero.hp,game.enemy.hp
