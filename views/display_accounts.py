import flask

from elthranonline import app
import services.decorators
import services.fetcher
import services.time
import models


# TODO refactor - this page does 3 things ... should only do 1.
@app.route('/display_accounts/<page_type>/<page_detail>/<descending>')
@app.route('/display_accounts/<page_type>/<page_detail>', methods=['GET', 'POST'])
@services.decorators.uses_hero
def display_accounts_page(hero=None, page_type=None, page_detail=None, descending=False):
    """Display all user accounts sorted on various columns.

    Consider adding bool converter <bool:descending>.
    http://flask.pocoo.org/docs/1.0/api/#url-route-registrations
    http://flask.pocoo.org/docs/1.0/api/#flask.Flask.url_map

    The if statement works and displays the account page as normal.
    Now if you click on a account it should run the else statement
    and pass in the account's username (which is unique). Now, I am
    having trouble sending the account to HTML. I can't seem to understand
    how to store the account information as a variable.
    """

    print(repr(descending))
    descending = False if descending == "False" or descending is False else True  # Because I am to lazy to write a converter
    print(repr(descending))

    if page_type == "display":
        sorted_heroes = services.fetcher.fetch_sorted_heroes(page_detail, descending)

        # Descending attribute inverted each time.
        return flask.render_template('accounts.html', page_title="Users", hero=hero, page_detail=page_detail, descending=not descending, all_heroes=sorted_heroes)

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
