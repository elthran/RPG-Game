import services.event_service


def move_hero(hero, location):
    """Move a hero to a new location."""
    hero.current_location = location

    if location not in hero.journal.known_locations:
        hero.journal.known_locations.append(location)

    # Set the hero's terrain to the terrain type of the place he just moved to.
    hero.current_terrain = location.terrain

    services.event_service.spawn(
        'move_event',
        hero,
        description="{} visits {}.".format(hero.name, location.url)
    )
