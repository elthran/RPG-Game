import flask

from elthranonline import app
import services.decorators


@app.route('/inventory_page')
@services.decorators.uses_hero
def inventory_page(hero=None):
    page_title = "Inventory"
    # for item in hero.inventory:
    #     if item.wearable:
    #         item.check_if_improvement()
    return flask.render_template('inventory.html', hero=hero, page_title=page_title, isinstance=isinstance, getattr=getattr)
