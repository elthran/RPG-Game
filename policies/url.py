from functools import wraps

from flask import session, request, flash
from werkzeug.utils import redirect

ALWAYS_VALID_URLS = [
    '/login', '/home', '/about', '/inventory_page', '/quest_log',
    '/attributes', '/proficiencies', '/ability_tree/*', '/bestiary/*',
    '/people_log/*', '/map_log', '/quest_log', '/display_users/*',
    '/inbox', '/logout',
]


# Work in progress.
# Control user moves on map. Rename too 'url_protect' because it sounds _sick_ :P.
def url_protect(f):
    """Redirects to last page if hero can't travel here.

    I need to update the location.py code to deal more with urls.
    """

    @wraps(f)
    def wrap_url(*args, **kwargs):
        #Currently disabled ... does nothing.
        return f(*args, **kwargs)


        # Break immediately if server is just being set up.
        # Everything after this will run just before the function
        # runs but not during function setup.
        # There is probably cleaner way?
        try:
            session['logged_in']
        except RuntimeError:
            return f(*args, **kwargs)

        # pprint(app.url_map)
        # pprint(args)
        # pprint(kwargs)
        # pprint(session)
        # print(dir(session))
        # f(*args, **kwargs)
        # print('after app.route')
        # print(dir(request.url_rule))
        # print("url rule", request.url_rule)
        # print("rule", request.url_rule.rule)
        # print("arguments", request.url_rule.arguments)
        # pprint(request)
        # print(dir(request))
        # print("Path requested: ", request.path)

        # Build requested move from rule and arguemts.
        valid_urls = ALWAYS_VALID_URLS

        hero = kwargs['hero']
        if hero.user.is_admin:
            valid_urls.append('/admin')

        # print("Hero current location url: ", hero.current_location.url)
        valid_urls.append(hero.current_location.url)
        valid_urls.append(hero.current_location.parent.url)
        for location in hero.current_location.adjacent:
            valid_urls.append(location.url)
        # Add this in later? Unless I can find out how
        # to do it another way.
        # local_places = hero.current_location.display.places_of_interest
        # print(hero.current_location)
        # pprint(hero.current_location.display.places_of_interest)
        # valid_urls += [] #all places of places_of_interest

        # This may work ... it will need more testing.
        # It may need additional parsing.
        requested_move = request.path
        # pdb.set_trace()
        if requested_move in valid_urls or hero.user.is_admin:
            # print("url is valid")
            session['last_url'] = request.path
            return f(*args, **kwargs)
        else:
            flash("You can't access '{}' from there.".format(requested_move))
            print("Possibly a bug in 'url_protect' .. possibly intended.")
            return redirect(session['last_url'])
    return wrap_url
