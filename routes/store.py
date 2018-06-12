import flask

from elthranonline import app
import services.decorators
import models


@app.route('/store/<name>')
@services.decorators.update_current_location
def store(name, hero=None, location=None):
    """Currently runs blacksmith and marketplace"""
    # print(hero.current_city)
    dialogue = None
    items_for_sale = []

    if name == "Blacksmith":
        dialogue = "I have the greatest armoury in all of Thornwall!"  # This should be pulled from pre_built objects
        items_for_sale = models.Item.filter_by(template=True).filter(models.Item.type != "Consumable").order_by(models.Item.name).all()
    elif name == "Marketplace":
        dialogue = "I have trinkets from all over the world! Please take a look."
        items_for_sale = models.Item.filter_by(template=True).filter_by(type="Consumable").all()
    else:
        error = "Trying to get to the store but the store name is not valid."
        flask.render_template('broken_page_link', error=error)
    return flask.render_template('store.html', hero=hero, dialogue=dialogue, items_for_sale=items_for_sale, page_title=location.display.page_title)
