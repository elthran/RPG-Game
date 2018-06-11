import services.fetcher


def add_quest_path_to_hero(hero, path_name):
    """Conveniently add a quest path to a hero.

    Modifies the hero object directly.
    Does nothing if hero already has this path.
    """
    if not services.fetcher.hero_has_quest_path_named(hero, path_name):
        new_path = services.fetcher.get_quest_path_template(path_name)
        hero.journal.quest_paths.append(new_path)
