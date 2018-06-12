import flask

from elthranonline import app
import services.decorators
import models


@app.route('/atlas/<int:map_id>')
@services.decorators.uses_hero
def atlas(hero=None, map_id=0):
    page_title = "Map"
    nodes = []
    possible_places = [hero.current_location.url]
    # Below is temporary map code as it's not currently set up
    all_maps = models.Location.filter_by(type='map').all()

    display_map = models.Location.get(map_id)
    # TODO refactor and interpret this code. Probably could use a different data structure?
    # Definitely a better way to do this ...
    # Maybe known locations could be a nodelist of some kind?
    for place in hero.current_location.places_of_interest['adjacent']:
        possible_places.append(place.url)
    if display_map:
        for child in display_map.children:
            if child in hero.journal.known_locations:
                print(child.name, child.point.x, child.point.y)
                if child.type == "town":
                    color = "red"
                elif child.type == "explorable":
                    color = "blue"
                elif child.type == "dungeon":
                    color = "green"
                else:
                    print("Location node has no known type: ", child.type)
                    color = "yellow"
                if child.url == hero.current_location.url:
                    url = "Self"
                elif child.url in possible_places:
                    url = child.url
                else:
                    url = "None"
                nodes.append((child, url, color))
    if nodes:
        print("Nodes: ", nodes)
        print("First node: ", nodes[0][0].point)
    return flask.render_template('journal.html', hero=hero, atlas=True, page_title=page_title, all_maps=all_maps, display_map=display_map, nodes=nodes)
