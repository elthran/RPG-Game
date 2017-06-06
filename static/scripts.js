/*global window, console*/
/*
Main command script that interacts with server through AJAX and
commands.py
*/
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
            } else if (action === "") {
                action = clickedButton.getAttribute("data-name");
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

/*
Unknown scripts (Marlen)
*/
// This is for the quest pop-up window. When the user clicks on div, open/close the popup
function quest_popup() {
    var popup = document.getElementById('js_popupachievement');
    popup.classList.toggle('show');
}

// This toggles whether or not you can see the battle log after a fight.
function battle_popup() {
    var x = document.getElementById('battle_log_div_id');
    if (x.style.display === 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }
}

/* 
Scrips for inventory page.

A script to hide the row in a table.
The element is hidden based on the button clicked having the same data value
as the id value of the table row id. These should both be unique.
*/
function removeRow(button) {
    "use strict";
    var tr = document.getElementById(button.getAttribute("data"));
    // console.log(tr);
    tr.style.display = "none";
    // button.style.display = 'none';
}

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

/*
Scripts for store to provide feedback when user buys something.
*/
function itemPurchasedPopup(button, message, heroGold) {
    var div = document.getElementById("purchaseLog");

    var para = document.createElement("p");
    var node = document.createTextNode(message);
    para.appendChild(node);
    div.insertBefore(para, div.firstChild);

    // Update hero gold
    var span = document.getElementById("heroGold");
    span.innerHTML = heroGold
}
