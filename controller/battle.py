# TODO Consider making this a module of its own. e.g. the battle module.
import combat_simulator


def setup_battle():
    """Determine which type of battle will occur and get an enemy."""
    pass


def setup_for_battle(hero):
    """Get an enemy hero to fight and attach some variables to them.

    This will need to be updated to query a hero object directly.
    These variables should probably be moved to the Game or Battle? objects.
    """
    # enemy.login_alerts += "You have been attacked!-"     This will be changed to the new notification system.
    hero.experience_rewarded = hero.age  # For now you just get 1 experience for each level the other hero was
    hero.items_rewarded = []   # Currently you get no items for killing another user


def battle(hero, enemy):
    setup_for_battle(hero)
    setup_for_battle(enemy)

    if hero and enemy and hero.is_alive() and enemy.is_alive():
        hero.battle_log = combat_simulator.battle_logic(hero, enemy)  # Not sure if the combat sim should update the database or return the heroes to be updated here
        enemy.battle_log = []
        if enemy.__class__.__name__ == "Hero":
            post_hero_battle(hero, enemy)
        else:
            post_monster_battle(hero, enemy)
        return hero.battle_log, enemy
    elif hero.is_dead():
        return ["You are to weak to fight!"], enemy
    elif enemy.is_dead():
        return ["{} is dead. Don't beat a dead horse!".format(enemy.name)], enemy


def post_hero_battle(hero, enemy):
    """Battle an enemy hero."""
    if hero.is_dead():  # First see if the player died.
        hero_died(hero, hero.battle_log)
        hero_won(enemy, hero, enemy.battle_log)
        enemy.journal.achievements.player_kills += 1
    else:  # Ok, the hero is not dead. Currently that means he won! Since we don't have ties yet.
        hero_died(enemy, enemy.battle_log)
        hero_won(hero, enemy, hero.battle_log)
        hero.journal.achievements.player_kills += 1  # You get a player kill score!


def post_monster_battle(hero, enemy):
    """Battle an enemy monster."""
    hero.current_dungeon_monster = False  # Whether you win or lose, the monster will now be gone.

    if hero.is_dead():  # First see if the player died.
        hero_died(hero, hero.battle_log)
        enemy.base_proficiencies['health'].current = enemy.base_proficiencies['health'].final  # auto-heal monster if it lives?
    else:  # Ok, the hero is not dead. Currently that means he won! Since we don't have ties yet.
        hero_won(hero, enemy, hero.battle_log)
        hero.journal.achievements.monster_kills += 1
        # TODO this should be hidden in some other code somewhere?
        enemy.delete()


def hero_died(hero, battle_log):
    """Modify the hero to accommodate death."""
    hero.current_location = hero.last_city  # Return hero to last visited city
    hero.current_dungeon_monster = False  # Reset any progress in any dungeon he was in
    hero.journal.achievements.deaths += 1  # Record that the hero has another death
    battle_log.append("You were defeated. You gain no experience and your account should be deleted.")


def hero_won(hero, enemy, battle_log):
    """Modify the hero to accommodate victory!"""
    experience_gained = hero.gain_experience(enemy.experience_rewarded)  # This works PERFECTLY as intended!

    if len(enemy.items_rewarded) > 0:  # Give the hero any items earned! This probably should be completely redone.
        reward_items(hero, enemy.items_rewarded)
    battle_log.append("You have defeated the " + enemy.name + " and gained " + str(experience_gained) + " experience!")


def reward_items(hero, items):
    """Reward any passed items to the hero."""
    for item in items:
        if not any(items.name == item.name for items in hero.inventory):
            hero.inventory.append(item)
        else:
            for item_owned in hero.inventory:
                if item_owned.name == item.name:
                    item_owned.amount_owned += 1
