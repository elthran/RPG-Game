from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *

def battle_logic():
    while myHero.hp > 0 and enemy.hp > 0:
        myHero.hp -= 1
        enemy.hp -= 5
        if myHero.hp < 0:
            myHero.hp = 0
        if enemy.hp < 0:
            enemy.hp = 0
    return myHero.hp,enemy.hp
