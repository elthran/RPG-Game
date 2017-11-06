"""
The command code is complicated and probably needs better naming separation.

As it stands it works like this:

# HTML
1. The user clicks on a prepared "Command" button.
The command button requires:
    a. data="data to send to python" - any kind you want
    b. data-py-function="the_name_of_a_python_function" - a static function in
        the commands.py module.
    c. data-js-callback="jsFunctionName" - (optional) js function to run that
        operates on the return values of the previous python function.

    e.g.
    <button
        data="{{ message.id }}"
        data-py-function="get_message_content_by_id"
        data-js-callback="divShow">
    </button>

# scripts.js
2. The user clicking on a "Command" button causes the "Command" script in
scripts.js to run.
The script adds in some data:
    a. python function name - "action" sent to the app.py Command code.
    b. the window location - in case you need this.
    c. the button "data" attribute - any kind of data you care to send.

    e.g.
    var action = clickedButton.getAttribute("data-py-function");
    xhttp.open(
        "GET",
        "/command/" + action + "?location=" + window.location.pathname
                + "&&data=" + clickedButton.getAttribute("data"),
        true
    );
    // and then we send it off
    xhttp.send();

# app.py
3. The Command code in app.py handles the data next. This adds some extra
info and attempts to run the appropriate Python function as specified in
the HTML
This operates like:
    a. cmd - name of the python function to run
    b. hero - current hero object
    c. database - current database object
    d. update the database.

    e.g.
    @app.route('/command/<cmd>')
    @uses_hero_and_update
    def command(cmd=None, hero=None):
        command_function = Command.cmd_functions(cmd)
        try:
            response = command_function(hero, database=database,
                                        arg_dict=request.args)
            database.update()
            # pdb.set_trace()
            return response
        except Exception as ex:
            raise ex

# commands.py
4. Run a python function based on the the HTML data and extra python data.
This looks like:
    a. consume == data-py-function value - function name
    b. hero - 1st arg, passed from app.py
    c. database - 2nd arg, passed from app.py
    d. data == 'data' from HTML - read only dictionary lookalike. Best to parse
        with '.get' as it allows typecasting and better error handling
    e. some operating code, the main point really :P.
    f. return value -- "success" is default. Other defaults are found in
        scripts.js line 60-71 ... "error: value" or "arg1&&arg2&&arg3"

    e.g.
    class Command
        @staticmethod
        def consume(hero, database, arg_dict):
            item_id = arg_dict.get('data', None, type=int)
            item = database.get_item_by_id(item_id)
            item.apply_effect(hero)
            database.delete_item(item_id)
            return "success"

# script.js
5. After python function returns run the js callback if one exists.
This looks like:
    a. If command.py reponse returns "Success" run a js function named
        with 'data-js-callback="someJSFunction"' passing the button in
        as the first and only argument.
OR
    b. If return starts with "error" print the text after that in the JS
        console.
OR
    c. run a JS function defined by 'data-js-callback' with the first arg
        being the button value and args 1, 2, 3, etc. being a list parsed
        as a string separated by '&&'. Please see script.js for comments.

    e.g.
    var clickedButton = e.target;
    var jsFunction = window[clickedButton.getAttribute("data-js-callback")];
    // If data-js-callback is not set then make a null function to
    // prevent errors.
    if (jsFunction === undefined) {
        jsFunction = function () {
            return;
        };
    }

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        // Wait until response gets full formed .. and isn't an error.
        if (xhttp.readyState === 4 && xhttp.status === 200) {
            if (xhttp.responseText === "success") {
                jsFunction(clickedButton);
            } else if (xhttp.responseText.substring(0, 5) === "error") {
                console.log("Python code returned an error from " + clickedButton);
                console.log(xhttp.responseText);
            } else {
                var requestArray = xhttp.responseText.split("&&");
                requestArray.unshift(clickedButton);
                jsFunction.apply(document, requestArray);
            }
        }
    };

# scripts.js and HTML
6. Run the JS callback function and modify the website HTML as needed.
This looks like:
    a. button is always arg1
    b. args2, args3 come from commands.py return value in the form
        return "args1&&arg2&&args3"


    e.g.
    function toggleEquip(button, itemType, idsArrayStr) {
        "use strict";
        //console.log(button);
        //console.log(itemType);
        //console.log(idsArray);
        var slot = document.getElementById(itemType);
        var tr = document.getElementById(button.getAttribute("data"));
        if (button.innerHTML === "Equip") {
            button.innerHTML = "Unequip";

            var idsArray = JSON.parse(idsArrayStr);
            idsArray.forEach(function (id) {
                //console.log("id: " + id);
                button = document.getElementById(id).querySelector("button");
                //console.log("Buttons to replace: " + button);
                //console.log("If button is real, data: " + button.getAttribute("data"))
                toggleEquip(button);
            });
            slot.insertAdjacentElement("afterend", tr);
        } else if (button.innerHTML === "Unequip") {
            slot = document.getElementById("non_equipped_items");
            button.innerHTML = "Equip";
            slot.appendChild(tr);
        }
    }
"""
