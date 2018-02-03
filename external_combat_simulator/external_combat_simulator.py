import sys
import time

from combat_formulas import *
from math import floor, sin
from random import randint, seed
from enum import Enum

# Enums
HEALTH = 1
ATTACK_SPEED = 2
FIRST_STRIKE = 3
ATTACK_ACCURACY = 4
ATTACK_DAMAGE = 5
CRITICAL_HIT = 6
EVADE = 7
BLOCK = 8
PARRY = 9	
RIPOSTE = 10
DEFENCE = 11
FATIGUE = 12

CURRENT_NUMBER_OF_PROFICIENCIES = 12
ALL_PROFICIENCIES = range(1,CURRENT_NUMBER_OF_PROFICIENCIES)

def get_proficiency(id):
    if id == HEALTH:
	    return "HEALTH"
    if id == ATTACK_SPEED:
	    return "ATTACK_SPEED"
    if id == FIRST_STRIKE:
	    return "FIRST_STRIKE"
    if id == ATTACK_ACCURACY:
	    return "ATTACK_ACCURACY"
    if id == ATTACK_DAMAGE:
	    return "ATTACK_DAMAGE"
    if id == CRITICAL_HIT:
	    return "CRITICAL_HIT"
    if id == EVADE:
	    return "EVADE"
    if id == BLOCK:
	    return "BLOCK"
    if id == PARRY:
	    return "PARRY"
    if id == RIPOSTE:
	    return "RIPOSTE"
    if id == DEFENCE:
	    return "DEFENCE"
    if id == FATIGUE:
	    return "FATIGUE"

def get_proficiencies_string(enum_list):
    result = []
    for num in enum_list:
        result.append(get_proficiency(num))
    return result

# Do not need to copy over
class Hero():
    """Store data about the Hero/Character object.

    """
    __tablename__ = 'hero'

    id = 1
    name = "hi"

    age = 7
    archetype = ""
    calling = ""
    religion = ""
    house = ""
    experience = 10
    experience_maximum = 10

    proficiencies_health_level = 0
    proficiencies_attack_speed_level = 0 
    proficiencies_first_strike_level = 0
    proficiencies_attack_accuracy_level = 0
    proficiencies_attack_damage_level = 0
    proficiencies_critical_hit_level = 0
    proficiencies_evade_level = 0
    proficiencies_block_level = 0 
    proficiencies_parry_level = 0
    proficiencies_riposte_level = 0
    proficiencies_defence_level = 0
    proficiencies_fatigue_level = 0
	
    proficiencies_health_current = 0
    proficiencies_attack_speed_speed = 0 
    proficiencies_first_strike_chance = 0
    proficiencies_attack_accuracy_accuracy = 0
    proficiencies_attack_damage_minimum = 0
    proficiencies_attack_damage_maximum = 0
    proficiencies_critical_hit_chance = 0
    proficiencies_critical_hit_modifier = 0
    proficiencies_evade_chance = 0
    proficiencies_block_chance = 0 
    proficiencies_block_modifier = 0
    proficiencies_parry_chance = 0
    proficiencies_riposte_chance = 0


    def __init__(self, **kwargs):
        #Defaults will remain unchanged if no arguments are passed.
        self.age = 7

        for key in kwargs:
            setattr(self, key, kwargs[key])
			
    def update(self):
        self.proficiencies_health_current = p_linear(self.proficiencies_health_level,5,0)
        #self.proficiencies_health_current = floor(5*self.proficiencies_health_level + 0)
		
        self.proficiencies_attack_damage_minimum = p_sinusoidal_linear(self.proficiencies_attack_damage_level,1,0,1,2)
        #self.proficiencies_attack_damage_minimum = floor(floor(3 * (0.5*sin(0.1*self.proficiencies_attack_damage_level) + 0.1*self.proficiencies_attack_damage_level)) + 0)

        self.proficiencies_attack_damage_maximum = p_sinusoidal_linear(self.proficiencies_attack_damage_level,2,0,1,2) 
        #self.proficiencies_attack_damage_maximum = floor(floor(3 * (0.5*sin(0.1*self.proficiencies_attack_damage_level) + 0.2*self.proficiencies_attack_damage_level)) + 1)	
		
        self.proficiencies_attack_speed_speed = p_sinusoidal_linear(self.proficiencies_attack_speed_level, 30, 300, 30, 2)
        #self.proficiencies_attack_speed_speed = round((3 * (0.1*sin(0.7*self.proficiencies_attack_speed_level) + 0.1*self.proficiencies_attack_speed_level)) + 1, 2)
		
        self.proficiencies_attack_accuracy_accuracy = p_increasing_bounded(self.proficiencies_attack_accuracy_level, 5, 50, 3)
        #self.proficiencies_attack_accuracy_accuracy = floor((- (10*5)/((2 * self.proficiencies_attack_accuracy_level) + 10) + 5) * 7.9 + 5)
        
        self.proficiencies_first_strike_chance = p_increasing_bounded(proficiencies_first_strike_level, -30, 50, 3)
        #self.proficiencies_first_strike_chance = floor((- (5*50)/((0.5 * self.proficiencies_first_strike_level) + 5) + 50) * 7.9 + -30)
		
        self.proficiencies_critical_hit_chance = p_increasing_bounded(self.proficiencies_critical_hit_level, -22, 50, 6)
        #self.proficiencies_critical_hit_chance = floor((- (5*50)/((0.3 * self.proficiencies_critical_hit_level) + 5) + 50) * 7.9 + -22)
		
        self.proficiencies_critical_hit_modifier = p_increasing_bounded(self.proficiencies_critical_hit_level, -22, 5, 4)
        #self.proficiencies_critical_hit_modifier = floor((- (1*0.5)/((0.5 * self.proficiencies_critical_hit_level) + 1) + 0.5) * 7.9 + 0)
		
        self.proficiencies_defence_modifier = p_increasing_bounded(self.proficiencies_defence_level, 0, 270, 4) 
        #self.proficiencies_defence_modifier = floor((- (7*35)/((0.1 * self.proficiencies_defence_level) + 7) + 35) * 7.9 + 0)
		
        self.proficiencies_evade_chance = p_increasing_bounded(self.proficiencies_evade_level, 0, 110, 4) 
        #self.proficiencies_evade_chance = floor((- (10*15)/((0.1 * self.proficiencies_evade_level) + 10) + 15) * 7.9 + 0)
		
        self.proficiencies_parry_chance = p_increasing_bounded(self.proficiencies_parry_level, 0, 115, 4)
        #self.proficiencies_parry_chance = floor((- (15*15)/((0.2 * self.proficiencies_parry_level) + 15) + 15) * 7.9 + 0)
		
        self.proficiencies_riposte_chance = p_increasing_bounded(self.proficiencies_riposte_level, 0, 120, 4)
        #self.proficiencies_riposte_chance = floor((- (20*15)/((0.3 * self.proficiencies_riposte_level) + 20) + 15) * 7.9 + 0)

        self.proficiencies_fatigue_maximum = p_linear(self.proficiencies_fatigue_level, 2, -1)
        #self.proficiencies_fatigue_maximum = floor(2*self.proficiencies_fatigue_level + -1)
		
        self.proficiencies_block_chance = p_increasing_bounded(self.proficiencies_block_level, 0, 430, 4)
        #self.proficiencies_block_chance = floor((- (25*60)/((0.25 * self.proficiencies_block_level) + 25) + 60) * 7.9 + 0)
        
        self.proficiencies_block_modifier = p_increasing_bounded(self.proficiencies_block_level, 0, 800, 4)
        #self.proficiencies_block_modifier = floor((- (20*100)/((1.5 * self.proficiencies_block_level) + 20) + 100) * 7.9 + 0)

    def set_level(self, enum, value):
        if enum == HEALTH:
            self.proficiencies_health_level = value
        elif enum == ATTACK_SPEED:		
            self.proficiencies_attack_speed_level = value
        elif enum == FIRST_STRIKE:		
            self.proficiencies_first_strike_level = value	
        elif enum == ATTACK_ACCURACY:		
            self.proficiencies_attack_accuracy_level = value	
        elif enum == ATTACK_DAMAGE:		
            self.proficiencies_attack_damage_level = value	
        elif enum == CRITICAL_HIT:		
            self.proficiencies_critical_hit_level = value	
        elif enum == EVADE:		
            self.proficiencies_evade_level = value
        elif enum == BLOCK:		
            self.proficiencies_block_level = value	
        elif enum == PARRY:		
            self.proficiencies_parry_level = value	
        elif enum == RIPOSTE:		
            self.proficiencies_riposte_level = value	
        elif enum == DEFENCE:		
            self.proficiencies_defence_level = value		
        elif enum == FATIGUE:		
            self.proficiencies_fatigue_level = value				

def determine_attacker(hero, monster):
    
	# Hero rolls first if hero has higher first strike chance
    if (hero.proficiencies_first_strike_chance > monster.proficiencies_first_strike_chance):
        if randint(0,100) < hero.proficiencies_first_strike_chance:
            #print ("Hero strikes first because of FIRST STRIKE!")
            return hero, monster
        if randint(0,100) < monster.proficiencies_first_strike_chance:
            #print ("Monster strikes first because of FIRST STRIKE!")
            return monster, hero  
    # Monster rolls first if monster has higher first strike chance
    elif (monster.proficiencies_first_strike_chance > hero.proficiencies_first_strike_chance):
        if randint(0,100) < monster.proficiencies_first_strike_chance:
            #print ("Monster strikes first because of FIRST STRIKE!")
            return monster, hero
        if randint(0,100) < hero.proficiencies_first_strike_chance:
            #print ("Hero strikes first because of FIRST STRIKE!")
            return hero, monster  
	# Draw or neither succeed in first strike	
    sum = abs(hero.proficiencies_attack_speed_speed + monster.proficiencies_attack_speed_speed)
    hero_chance = (hero.proficiencies_attack_speed_speed/sum)*100 + randint(-20,20)
    #print ("Chance for HERO to attack this round: " + str(hero_chance) + "%")
    if randint(0,100) < hero_chance:
	    return hero, monster
    return monster, hero

def determine_if_hits(accuracy):
    #print ("Chance for attacker to hit their opponent is: " + str(accuracy) + "%")
    if randint(0,100) <= accuracy:
        return True
    return False

def determine_if_critical_hit(chance):
    #print ("Chance for critical hit is: " + str(chance) + "%")
    if randint(0,100) < chance:
        return True
    return False

def calculate_damage(minimum, maximum):
    if maximum <= minimum:
        maximum = minimum + 1 # This avoids a bug with randint looking at impossible ranges
    damage = randint(minimum, maximum)
    #print ("Unmodified attack will hit for this much damage: " + str(damage))
    return damage

def critical_hit_modifier(original_damage, modifier):
    #print ("Critical hit! Damage multiplied by: " + str(modifier))
    damage = original_damage * modifier
    return damage

def determine_evade(chance):
    #print ("Chance to evade is: " + str(chance) + "%")
    if randint(0,100) < chance:
        return True	
    return False

def determine_block_chance(chance):
    #print ("Chance to block is: " + str(chance) + "%")
    if randint(0,100) < chance:
        return True
    return False

def determine_block_amount(original_damage, modifier):
    #print ("You will block this percent of damage: " + str(modifier) + "%")
    damage = original_damage * (1 - modifier)
    if damage < 1:
        damage = 1
    return damage

def determine_parry_chance(chance):
    #print ("Chance to parry is: " + str(chance) + "%")
    if randint(0,100) < chance:
        return True
    return False

def determine_riposte_chance(chance):
    #print ("Chance to riposte is: " + str(chance) + "%")
    if randint(0,100) < chance:
        return True
    return False


	
def battle_logic(active_player, inactive_player):
    """ Runs the entire battle simulator """
    combat_log = [active_player.name + " Health: " + str(active_player.proficiencies_health_current) + "  " + inactive_player.name + " Health: " + str(inactive_player.proficiencies_health_current)]
    while (active_player.proficiencies_health_current > 0) and (inactive_player.proficiencies_health_current > 0):
        damage = 0
        attacker, defender = determine_attacker(active_player, inactive_player)
        if determine_if_hits(attacker.proficiencies_attack_accuracy_accuracy):
            damage = calculate_damage(attacker.proficiencies_attack_damage_minimum, attacker.proficiencies_attack_damage_maximum)
        else:
            #combat_log.append(attacker.name + " misses!")
            continue
        if determine_if_critical_hit(attacker.proficiencies_critical_hit_chance):
            damage = critical_hit_modifier(damage, attacker.proficiencies_critical_hit_modifier)
        if determine_evade(defender.proficiencies_evade_chance):
            combat_log.append(str(defender.name) + " evaded!")
            continue
        if determine_block_chance(defender.proficiencies_block_chance):
            #combat_log.append(str(defender.name) + " blocked some damage!")
            damage = determine_block_amount(damage, defender.proficiencies_block_modifier)
        if determine_parry_chance(defender.proficiencies_parry_chance):
            continue
        if determine_riposte_chance(defender.proficiencies_riposte_chance):
            continue
        if damage < 0:
            damage = 0
        defender.proficiencies_health_current -= damage
        #print("defender health ", defender.proficiencies_health_current, attacker.proficiencies_health_current)
        #combat_log.append("%s hits for %i. %s has %i health left.\n" % (attacker.name, damage, defender.name, defender.proficiencies_health_current))
    if active_player.proficiencies_health_current <= 0:
        active_player.proficiencies_health_current = 0
        #combat_log.append(active_player.name + " is dead")
    else:
        inactive_player.proficiencies_health_current = 0
        #combat_log.append(inactive_player.name + " is dead.\nYou gain experience.")
    return active_player.proficiencies_health_current #active_player.proficiencies_health_current, inactive_player.proficiencies_health_current, combat_log

def create_average_hero(average_level):
    hero = Hero()
    hero.proficiencies_attack_damage_level = average_level
    hero.proficiencies_health_level = average_level
    hero.proficiencies_attack_speed_level = average_level
    hero.proficiencies_first_strike_level = average_level
    hero.proficiencies_attack_accuracy_level = average_level
    hero.proficiencies_attack_damage_level = average_level
    hero.proficiencies_critical_hit_level = average_level
    hero.proficiencies_evade_level = average_level
    hero.proficiencies_block_level = average_level
    hero.proficiencies_parry_level = average_level
    hero.proficiencies_riposte_level = average_level
    hero.proficiencies_defence_level = average_level
    hero.proficiencies_fatigue_level = average_level
    hero.update()
    return hero

# returns the distribution of level points for each proficiency ordered based 
# on list_of_biased_proficiencies in create_biased_hero
def create_biased_hero_helper(num_of_biased,total_level_points):
    result = []
    num_of_non_biased = CURRENT_NUMBER_OF_PROFICIENCIES - num_of_biased
    points_for_biased = total_level_points - num_of_non_biased
    num_of_floor = num_of_biased - (points_for_biased % num_of_biased)
    floor_value = floor(points_for_biased / num_of_biased)
    for i in range(0,num_of_floor):
        result.append(floor_value)
    for i in range(num_of_floor,num_of_biased):
        result.append(floor_value + 1)
    for i in range(num_of_biased,CURRENT_NUMBER_OF_PROFICIENCIES):
        result.append(1)	
    return result
	
# creates a hero that is biased in proficiencies	
def create_biased_hero(list_of_biased_proficiencies,average_level):
    hero = Hero()
    total_level_points = CURRENT_NUMBER_OF_PROFICIENCIES * average_level
    distribution = create_biased_hero_helper(len(list_of_biased_proficiencies),total_level_points)
    #print(distribution)
    for i in range(0,CURRENT_NUMBER_OF_PROFICIENCIES):
        hero.set_level(i,1)
    for i in range(0,len(list_of_biased_proficiencies)):
        hero.set_level(list_of_biased_proficiencies[i], distribution[i])
    hero.update()
    return hero
	
# returns the win rate of the hero
def get_win_rate(hero, monster, simulation_count):
    wins = 0
    for n in range(0,simulation_count):
        result = battle_logic(hero, monster)
        hero.update()
        monster.update()
        #print("print result, ",result)
        if result != 0:
            wins += 1
    return wins/simulation_count		

# hero_list : list of enums representing proficiencies that the hero is biased towards
# monster_list : list of enums representing proficiencies that the monster is biased towards
# example:
# output_battle_data([ATTACK_ACCURACY],ALL_PROFICIENCIES,5,100)
# would make a hero with almost all proficiencies added to ATTACK_ACCURACY battle 
# monster with evenly spread proficiencies (biased towards ALL_PROFICIENCIES = evenly spread)
# the result will be a 5 by 5 grid, and each battle will be conducted 100 times
# uncomment the code inside the function to have it output to an external txt file
def output_battle_data(hero_list, monster_list, max_proficiency_level, simulation_count):
    #orig_stdout = sys.stdout
    #f = open('out.txt', 'w')
    #sys.stdout = f
    print("This is the output file for a battle simulation. Here are some info:")
    print("Hero is biased towards these proficiencies: " + str(get_proficiencies_string(hero_list)) + ".")
    print("Monster is biased towards these proficiencies: " + str(get_proficiencies_string(monster_list)) + ".")
    print("Simulation is done " + str(simulation_count) + " number of times for each block on the grid.")
    print("The x-axis is the average proficiency level of the monster.")
    print("The y-axis is the average proficiency level of the hero.")
    print("")
    first_row = "   "
    for monster_level in range(1, max_proficiency_level+1):
        first_row += str(monster_level) + "    "
    print(first_row)
    for hero_level in range(1,max_proficiency_level+1):
        row = str(hero_level) + "  "
        for monster_level in range(1, max_proficiency_level+1):
            hero = create_biased_hero(hero_list, hero_level)
            monster = create_biased_hero(monster_list, monster_level)
            row += "{0:.2f}".format(get_win_rate(hero, monster, simulation_count)) + " " 	
        print(row)
    #sys.stdout = orig_stdout
    #f.close()
       
output_battle_data([CRITICAL_HIT],ALL_PROFICIENCIES,10,20)

# testing functions
#print(get_win_rate(create_biased_hero(ALL_PROFICIENCIES, 2),create_biased_hero(ALL_PROFICIENCIES, 3),10))
#print(determine_attacker(create_biased_hero(ALL_PROFICIENCIES, 3),create_biased_hero(ALL_PROFICIENCIES, 3)))
