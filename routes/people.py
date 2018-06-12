from flask import render_template

from elthranonline import app
import models
import services.decorators


@app.route('/people_log/<int:npc_id>')
@services.decorators.uses_hero
def people_log(hero=None, npc_id=0):
    page_title = "People"
    all_npcs = models.NPC.all()
    display_npc = models.NPC.get(npc_id)
    return render_template('journal.html', hero=hero, people_log=True, page_title=page_title, all_npcs=all_npcs, display_npc=display_npc)
