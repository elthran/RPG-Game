# TODO: update documentation!
Run a list of html update commands based on the string cmd.

## Usage: _elthranonline/\_\_init\_\_.py_
`import routes.command`

## Usage: _routes/command.py_
```python
command_function = commands.cmd_functions(cmd)
if flask.request.method == 'POST' and flask.request.is_json:
    try:
        data = flask.request.get_json()
    except werkzeug.exceptions.BadRequest as ex:
        raise Exception(str(ex))
    response = command_function(hero, data=data)
else:
    response = command_function(hero, arg_dict=flask.request.args)
return response
```
## Usage: _commands/\_\_init\_\_.py_
```python
from .message import get_message_content_and_sender_by_id
from .notification import send_notification_data
# ... etc

def cmd_functions(name):
    """Use to refer to return a function from string of its name.

    Getattr wrapper ...
    """
    try:
        return globals()[name]
    except KeyError as ex:
        raise Exception("You need to write a function called '{}' in commands/ package and import it into the commands.__init__.py file.".format(name))
```

## Usage: _commands/buy_item.py_
```python
def buy_item(hero, data=None, *args, **kwargs):
    """Allow the hero to buy items from the Blacksmith.

    Returns an error if the character doesn't have enough gold.
    """
    item_id = data['id']
    location = data['location']
    item = services.generators.create_item(item_id)
    if hero.gold >= item.buy_price:
        hero.inventory.add_item(item)
        hero.gold -= item.buy_price
        services.event_service.spawn(
            'buy_event',
            hero,
            description="{} buys a/an {}.".format(hero.name, item.name)
        )
        return flask.jsonify(
            message="Purchased: {}: id={}".format(item.name, item.id),
            heroGold=hero.gold)
    return flask.jsonify(error="Not enough gold to buy '{}'!".format(item.name))
```

## Usage: _store.html_
```html
<button onclick="sendToPy(event, itemPurchasedPopup, 'buy_item', {'id': {{ item.id }}});">Buy</button>
```
NOTE: the data is sent as JSON, HTML is actually a Jinja2 template ...

## Usage: _script.js_
```javascript
function sendToPy(event, callback, cmd, data, preProcess, url) {
    "use strict";
    // Default arguments [equivalent to "def f(data='')" in python]
    // If data is undefined it will cause the python code to throw
    // as 400 (bad response) server error when it tries to decode the
    // JSON data. If the server can't decode the data it now loudly
    // throws a 400 error. I hope this is a good idea.
    // The data sent _must_ be valid JSON data.
    if (data === undefined) {
        data = ""
    }

    var element = event.target;

    if (cmd && url) {
        throw "Use a cmd or a url not both!";
    }
    if (data && preProcess) {
        throw "Use preProcess or data not both!";
    }

    if (cmd) {
        url = "/command/" + cmd;
    } else if (!cmd && !url) {
        // if url is blank use url of page
        url = window.location.pathname;
    }

    // Normal data processing is object form.
    // Must return a JSON object - no I can't check for this.
    if (preProcess) {
        data = preProcess(element);
    }

    // If you send a simple string location won't be added.
    // If you send (hopefully) some JSON the location parameter will be added.
    if (typeof data !== "string") {
        // If there is some (JSON type data) add in the location variable.
        data.location = window.location.pathname;
    }

    postJSON(url, data, callback);

    // For normal event suppression.
    event.preventDefault();
    // Extra event suppression
    event.stopPropagation();
    // For form submit suppression
    return false;
}

// Send the data via POST to the server. Run callback if it exists.
// Sends data as JSON. Customizable.
// Pre-parses responseText if the ResponseHeader is JSON type.
function postJSON(url, oldData, callback) {
    "use strict";
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4 && xhttp.status === 200) {
            if (callback) {
                // If the python code returns JSON formatted data:
                // 1. run the "notification" code if that flag was passed.
                // 2. send only the data to the callback.
                if (xhttp.getResponseHeader("Content-Type") === "application/json") {
                    var response = JSON.parse(xhttp.responseText);
//                    showGlobalNotificationButton(response["isNotice"], true);
                    callback(response, oldData);
                // If the python code sends back an error i.e. "return "error: ...."
                // print it to the console.
                } else if (xhttp.responseText.substring(0, 5) === "error") {
                        console.log("Python code returned an error:");
                        console.log(xhttp.responseText);
                // Otherwise handle it by passing the response to the callback.
                // The callback function will need to parse the xhttp personally.
                } else {
                    callback(xhttp, oldData);
                }
                // if you want to reload the page?
                // window.location.replace(url);
            }
        }
    };
    xhttp.open("POST", url, true);
    var JSONdata = JSON.stringify(oldData);
    console.log("Data to be sent: " + JSONdata);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSONdata);
}
```

#### NOTES:
- Go to the real code for most up to date documentation and examples.
- preProcess is the name of whatever JS function you want to use
to extract the data from the HTML.

Usage: _scripts.js > getIdsFromCheckboxes_

See: 'inbox.html'
```html
<input type="submit" name="delete" form="messageForm" value="DELETE"
onclick="return sendToPy(
    event, updateMessageTable, null, null, getIdsFromCheckboxes);"/>
```
