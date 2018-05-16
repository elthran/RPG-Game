import flask

from elthranonline import app
import services.decorators
import services.fetcher
import services.time
import models


@app.route('/display_accounts/<page_type>/<page_detail>', methods=['GET', 'POST'])
@services.decorators.uses_hero
def display_accounts_page(page_type, page_detail, hero=None):
    descending = False
    if page_detail == hero.clicked_user_attribute:
        hero.clicked_user_attribute = ""
        descending = True
    else:
        hero.clicked_user_attribute = page_detail

    if page_type == "display":
        sorted_heroes = services.fetcher.fetch_sorted_heroes(page_detail, descending)
        return flask.render_template(
            'accounts.html', page_title="Users", hero=hero,
            page_detail=page_detail, all_heroes=sorted_heroes)
    elif page_type == "see_account":
        this_user = models.Account.filter_by(username=page_detail)
        this_hero = services.fetcher.fetch_hero_by_username(page_detail)
        # Below code is just messing with inbox
        if flask.request.method == 'POST':
            this_message = flask.request.form['message']
            if len(this_message) > 1:
                hero.account.inbox.send_message(this_user, this_message, services.time.now())
                confirmation_message = "Message sent!"
            else:
                confirmation_message = "Please type your message"
            return flask.render_template('profile_other_user.html', hero=hero, page_title=str(this_user.username), enemy_hero=this_hero, confirmation=confirmation_message)
        # Above this is inbox nonsense
        return flask.render_template('profile_other_user.html', hero=hero, page_title=str(this_user.username), enemy_hero=this_hero)
