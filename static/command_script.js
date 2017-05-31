/*global window, console*/
// Only run what comes next *after* the page has loaded
document.addEventListener("DOMContentLoaded", function () {
    "use strict";
    // Grab all of the elements with a class of command
    // (which all of the buttons we just created have)
    var commandButtons = document.querySelectorAll(".command");

    // As commandButtons is a NodeList ... foreach shouldn't work
    // but it does. This may cause browsers incompatabilites?
    // If this becomes a problem use:
    // var i = 0;
    // var button = {};
    // for (i = 0; i < commandButtons.length; i += 1) {
    //     button = commandButtons[i];
    // }
    // Iterate through the NodeList created by "querySelectorAll"
    commandButtons.forEach(function (button) {
        // For each button, listen for the "click" event
        button.addEventListener("click", function (e) {
            // When a click happens, stop the button
            // from submitting our form (if we have one)
            e.preventDefault();

            var clickedButton = e.target;
            var dataFunction = window[clickedButton.getAttribute("data-function")];

            // If data-function is not set then make a null function to prevent errors.
            if (dataFunction === undefined) {
                dataFunction = function () {
                    return;
                };
            }

            // Now we need to send the data to our server
            // without reloading the page - this is the domain of
            // AJAX (Asynchronous JavaScript And XML)
            // We will create a new request object
            // and set up a handler for the response
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                // Wait until response gets full formed .. and isn't an error.
                if (xhttp.readyState === 4 && xhttp.status === 200) {
                    // Execute a secondary function stored on the button.
                    // Replicates <button onClick=fn(this)> but where the secondary
                    // function occurs AFTER the response (and only on valid responses).
                    if (xhttp.responseText === "success") {
                        dataFunction(clickedButton);
                    } else if (xhttp.responseText.substring(0, 5) === "error") {
                        console.log("Python code returned an error from " + clickedButton);
                        console.log(xhttp.responseText);
                    } else {
                        // Current response format must be of the form arg2&&arg3&&arg4.
                        // arg1 is always the button clicked.
                        // I will put some error checking in to make sure that this happens at some point.
                        var requestArray = xhttp.responseText.split("&&");
                        requestArray.unshift(clickedButton);
                        dataFunction.apply(document, requestArray);
                    }
                }
            };
            // We point the request at the appropriate command
            // Send data to python. To send non string args you must not use the "+" operator.
            // Then you can send the data raw or in lots of other formats.
            // See https://www.w3schools.com/xml/ajax_xmlhttprequest_send.asp
            // "&&" acts like the "," in pythonic {key:value, key2:value2}

            // "innerHTML was quick and simple and didn't account for having complex buttons
            // and now I will need to switch over to using the "name" attribute.
            // use of "innerHTML" will cause conflict in the future but it is here now.
            var action = clickedButton.innerHTML.toLowerCase();
            if (action === "") {
                action = clickedButton.getAttribute("name");
            }
            //console.log("action if name: " + action);

            //get buttons class and save it as the .
            console.log("Button clicked was:", clickedButton);

            // innerHTML for a button is the button's "label" (the part you see).
            xhttp.open(
                "GET",
                "/" + action + "?location=" + window.location.pathname + "&&data=" + clickedButton.getAttribute("data"),
                true
            );
            // and then we send it off
            xhttp.send();
        });
    });
}, true);