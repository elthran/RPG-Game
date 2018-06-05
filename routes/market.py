import flask

from elthranonline import app
import services.decorators
import models


# TODO not sure if this code is still alive? Or if it is just a remnant.
@app.route('/marketplace/<inventory>')
@services.decorators.uses_hero
def marketplace(inventory, hero=None):
    if inventory == "shopping":
        items_for_sale = models.Item.filter_by(template=True, type="Consumable").all()
        dialogue = "Anything catch your fancy?"
    else:
        items_for_sale = []
        dialogue = "Welcome to the Thornwall market. We have goods from all over the eastern coast. Come in and take a look."
    return flask.render_template('store.html', hero=hero, items_for_sale=items_for_sale, dialogue=dialogue)  # return a string
