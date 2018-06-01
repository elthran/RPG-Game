import pdb

import flask
import werkzeug.exceptions

from elthranonline import app
import services.decorators
import controller.commands


# Implement Security Policies here?
@app.route('/command/<cmd>', methods=['GET', 'POST'])
@services.decorators.uses_hero
def command(cmd=None, hero=None):
    """Accept a string from HTML button code -> send back a response.

    The response must be in the form: "key=value" (at this time.)
    See the Command class in the commands.py module.
    cmd is equal to the value of the value field in the html code
    i.e. <button value='foo'> -> cmd == 'foo'

    Extra data can be sent in request.args (which is accessible from within this namespace).

    args are sent in the form "/" + command + "?key=value&&key2=value2".
    Where the value of command == cmd and
    args == {key: value, key2: value2} (well it isn't a real dict but it mostly acts like one).

    Or you could sent the data as a file ... or raw or some XML or something
    and then parse it on this end based on the headers. But that is more complicated
    than I need right now.

    NOTE: Need to make sure this doesn't conflict with other routes
    """

    testing = False  # True/False
    if testing:
        print('request is:', repr(flask.request))
        # print('request data:', repr(request.data))
        # print("request form:", repr(request.form))
        print('request view_args:', repr(flask.request.view_args))
        print('request args:', repr(flask.request.args))
        print('cmd is:', repr(cmd))

    # event = Event(request.args)
    # event.add["hero"] = hero
    # event.add["database"] = database

    response = None
    try:
        # command_function = getattr(globals(), <cmd>)
        # response = command_function(hero, javascript_kwargs_from_html)
        command_function = controller.commands.cmd_functions(cmd)
    except AttributeError as ex:
        if str(ex) == "type object 'Command' has no attribute '{}'".format(
                cmd):
            print("You need to write a function called '{}' in "
                  "controller/commands.py.".format(cmd))
            raise ex
        raise ex

    if flask.request.method == 'POST' and flask.request.is_json:
        try:
            data = flask.request.get_json()
        except werkzeug.exceptions.BadRequest as ex:
            # This might be a terrible idea as maybe it lets people crash
            # the server by sending invalid data?
            # I figure that this error shouldn't pass silently with no idea
            # what caused it.
            raise Exception(str(ex))
        response = command_function(hero, data=data)
    else:
        response = command_function(hero, arg_dict=flask.request.args)
    # pdb.set_trace()
    return response
