/*global window, console*/
/*
Main command script that interacts with server through AJAX and
commands.py
*/
// Only run what comes next *after* the page has loaded

// OFFICIAL NAME: js EventListener code??
document.addEventListener("DOMContentLoaded", function () {
    "use strict";
    // Grab all of the elements with a class of command
    // (which all of the buttons we just created have)
    // var commandButtons = document.querySelectorAll(".command");
    var commandButtons = document.querySelectorAll("[data-py-function]");

    // As commandButtons is a NodeList ... foreach shouldn't work
    // but it does. This may cause browsers incompatibilities?
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
            // Bubbles Event until it hits py call
            // This is useful for using a div as the sender.
            while (!clickedButton.getAttribute("data-py-function")) {
                clickedButton = clickedButton.parentElement;
            }

            // Build a handler to a function named in data-js-callback if one
            // exists.
            var jsFunction = window[clickedButton.getAttribute("data-js-callback")];
            // If data-js-callback is not set then make a null function to
            // prevent errors.
            if (jsFunction === undefined) {
                jsFunction = function () {
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

                    // e.g. from Python 'equip' -> return item.type + "&&" + str(ids_to_unequip)
                    // Sends a list of ids to be toggled.
                    // in JS -> toggleEquip(button, itemType, idsArrayStr)
                    // Accepts 'button' as default arg ... plus the item.type and
                    // list of ids.
                    if (xhttp.responseText === "success") {
                        jsFunction(clickedButton);
                    } else if (xhttp.responseText.substring(0, 5) === "error") {
                        console.log("Python code returned an error from " + clickedButton);
                        console.log(xhttp.responseText);
                    } else {
                        // Current response format must be of the form arg2&&arg3&&arg4.
                        // arg1 is always the button clicked.
                        // I will put some error checking in to make sure that this happens at some point.
                        var requestArray = xhttp.responseText.split("&&");
                        requestArray.unshift(clickedButton);
                        jsFunction.apply(document, requestArray);
                    }
                }
            };
            // We point the request at the appropriate command
            // Send data to python. To send non string args you must not use the "+" operator.
            // Then you can send the data raw or in lots of other formats.
            // See https://www.w3schools.com/xml/ajax_xmlhttprequest_send.asp
            // "&&" acts like the "," in pythonic {key:value, key2:value2}

            // The value of data-py-function should be the name of a
            // @staticmethod in the Command class in the commands.py file.
            var action = clickedButton.getAttribute("data-py-function");

            // console.log("action_final:", action)
            console.log("Button clicked was:", clickedButton);
            // Send this to the Python app.py 'url.route(/command/<cmd>)'
            xhttp.open(
                "GET",
                "/command/" + action + "?location=" + window.location.pathname
                        + "&&data=" + clickedButton.getAttribute("data"),
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

function refreshPage() {
    location.reload();
}

function show(element) {
    element.classList.remove('hide')
    element.classList.add('show')
}

function hide(element) {
    element.classList.remove('show')
    element.classList.add('hide')
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

Currently handles unequip and equipping one item at at time.
The current approach is not very flexible.
*/
function toggleEquip(clicked, slot_type, idsArrayStr) {
    "use strict";
//    log("toggleEquip function");
//    console.log(clicked);
//    console.log(slot_type);
//    console.log(idsArrayStr);
    var tooltipDiv = clicked;
    var inventoryItemDiv = tooltipDiv.parentElement;
    var empty_slot = document.getElementById("inventory-" + slot_type + "-empty");
//    console.log(empty_slot);

    var command = tooltipDiv.getAttribute("data-py-function");

    // When you are Unequipping an Item.
    if (command === "unequip") {
        inventoryItemDiv.removeChild(tooltipDiv);
        empty_slot.style.display = "inline";

        tooltipDiv.setAttribute("data-py-function", "equip");

        var unequippedItemDiv = document.createElement("div");
        unequippedItemDiv.classList.add("inventory-unequipped", "inventory-item");
        unequippedItemDiv.appendChild(tooltipDiv);

        var unequippedGeneralDiv = document.getElementById("unequipped");
        unequippedGeneralDiv.appendChild(unequippedItemDiv);

    // When you are Equipping and Item.
    } else if (command === "equip") {
        inventoryItemDiv.parentElement.removeChild(inventoryItemDiv);
        empty_slot.style.display = "none";

        tooltipDiv.setAttribute("data-py-function", "unequip");
        var slotDiv = document.getElementById("inventory-" + slot_type);
        slotDiv.appendChild(tooltipDiv);
    }
}

/*
Scripts for store to provide feedback when user buys something.
*/
function itemPurchasedPopup(response) {
    "use strict";

    var message;
    if (response.error) {
        message = response.error;
    } else {
        message = response.message;
        // Update hero gold
        var span = document.getElementById("heroGold");
        span.innerHTML = response.heroGold;
    }

    var div = document.getElementById("purchaseLog");

    var para = document.createElement("p");
    var node = document.createTextNode(message);
    para.appendChild(node);
    div.insertBefore(para, div.firstChild);
}

// This function is used in the profile_proficiencies.html
// This function only runs if command code return successfully from Python.
// Could be updated to just rerender all html for tooltip :P
function attributeTooltip(button, tooltip) {
    var newTooltip = {};
    newTooltip = document.getElementById("attributeTooltip");
    newTooltip.innerHTML = tooltip;
}

function updateAttribute(button, status) {
    "use strict";
    var id = 0;
    var i = 0;
    var heroAtrPointsDiv = {};
    var atrCurrentLvDiv = {};
    var buttonsNodeList = {};
    id = button.getAttribute("data");
    atrCurrentLvDiv = document.getElementById("attribute-" + id);
    heroAtrPointsDiv = document.getElementById("points_remaining");
    atrCurrentLvDiv.innerHTML = parseInt(atrCurrentLvDiv.innerHTML) + 1;
    heroAtrPointsDiv.innerHTML = parseInt(heroAtrPointsDiv.innerHTML) - 1;
    if (status === "hide_all") { //hide all buttons
        buttonsNodeList = document.querySelectorAll("button[class=upgradeButton]");
        for (i = 0; i < buttonsNodeList.length; i++) {
            buttonsNodeList[i].style.display = "none";
        }
    }
}

function proficiencyTooltip(button, tooltip) {
    var newTooltip = {};
    newTooltip = document.getElementById("proficiencyTooltip");
    newTooltip.innerHTML = tooltip;
}

function updateProficiency(button, status, tooltip) {
    "use strict";
    proficiencyTooltip(button, tooltip);
    var id = 0;
    var i = 0;
    var heroProfPointsDiv = {};
    var profCurrentLvDiv = {};
    var buttonsNodeList = {};
    id = button.getAttribute("data");
    profCurrentLvDiv = document.getElementById("proficiency-" + id);
    heroProfPointsDiv = document.getElementById("points_remaining");
    profCurrentLvDiv.innerHTML = parseInt(profCurrentLvDiv.innerHTML) + 1;
    heroProfPointsDiv.innerHTML = parseInt(heroProfPointsDiv.innerHTML) - 1;
    if (status === "hide_this") { //hide this button
        button.style.display = "none";
    } else if (status === "hide_all") { //hide all buttons
        buttonsNodeList = document.querySelectorAll("button[class=upgradeButton]");
        for (i = 0; i < buttonsNodeList.length; i++) {
            buttonsNodeList[i].style.display = "none";
        }
    }
}

function abilityTooltip(button, tooltip, image) {
    var newTooltip = {};
    var newImage = {};
    var startImage = '<img src="/static/images/';
    var endImage = '.jpg" alt="none">';
    newTooltip = document.getElementById("attributeTooltip");
    newTooltip.innerHTML = tooltip;
    newImage = document.getElementById("attributeImage");
    newImage.innerHTML = startImage + image + endImage;
}

function updateAbility(button, status, tooltip) {
    "use strict";
    var id = 0;
    var i = 0;
    var heroAbiPointsDiv = {};
    var abiCurrentLvDiv = {};
    var buttonsNodeList = {};
    var newTooltip = {};
    newTooltip = document.getElementById("attributeTooltip");
    newTooltip.innerHTML = tooltip;
    id = button.getAttribute("data");
    abiCurrentLvDiv = document.getElementById("ability-" + id);
    heroAbiPointsDiv = document.getElementById("points_remaining");
    abiCurrentLvDiv.innerHTML = parseInt(abiCurrentLvDiv.innerHTML) + 1;
    heroAbiPointsDiv.innerHTML = parseInt(heroAbiPointsDiv.innerHTML) - 1;
    if (status === "hide_this") { //hide this button
        button.style.display = "none";
    } else if (status === "hide_all") { //hide all buttons
        buttonsNodeList = document.querySelectorAll("button[class=upgradeButton]");
        for (i = 0; i < buttonsNodeList.length; i++) {
            buttonsNodeList[i].style.display = "none";
        }
    }
}

function abilityChoiceTooltip(button, description, image) {
    var newTooltip = {};
    var newImage = {};
    var startImage = '<img src="/static/images/';
    var endImage = '.jpg" alt="none">';
    newTooltip = document.getElementById("abilityChoiceTooltip");
    newTooltip.innerHTML = description;
    newImage = document.getElementById("choiceImage");
    newImage.innerHTML = startImage + image + endImage;
}

function questTooltip(button, description, image) {
    var newTooltip = {};
    var newImage = {};
    var startImage = '<img src="/static/images/';
    var endImage = '.jpg" alt="none">';
    newTooltip = document.getElementById("questTooltip");
    newTooltip.innerHTML = description;
    newImage = document.getElementById("choiceImage");
    newImage.innerHTML = startImage + image + endImage;
}

function pageReload(button) {
    location.reload();
}

function showGlobalModal(button) {
    // Get the modal
    var modal = document.getElementById('globalMessage');
    // Get the button that opens the modal
    var clickedButton = document.getElementById("globalNotificationButton");
    // Get the <span> element that closes the modal
    var span = document.querySelector(".closeGlobalModal");
    // When the user clicks the button, open the modal
    modal.style.display = "block";
    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Handle ESC key (key code 27) to close modal.
    document.addEventListener('keyup', function(event) {
        if (event.keyCode == 27) {
            modal.style.display = "none";
        }
    });

    clickedButton.style.display = "none";
}

// Choose character page, confirms user choice of hero.
function confirmHeroSelection(element) {
    // Should bring up a confirmation dialogue or something.
    console.log("The confirm hero selection JS should really have some kind of confirmation dialogue.");
    if (true) {
        formHeroIDInput = document.querySelector("[name=hero_id]");
        formHeroIDInput.value = element.id;
        return true;
    } else {
        return false;
    }

}

// Inbox Reply popup

//Function To Display Popup
function popupReplyBox(button, messageContent, messageSender) {
    // Here we need to add some JS to make the message no longer bold, as it is no longer unread
    document.getElementById('inboxPopupWindow').style.display = "block";

    var contentInput = document.querySelector("[name=content]");

    if (contentInput) {
        contentInput.focus();
    }
    document.getElementById('replyBoxMessageContent').innerHTML = messageContent;
    document.getElementById('replyBoxMessageSender').innerHTML = messageSender;
    document.querySelector("[name=message_id]").value = button.getAttribute("data");
}

function newPopupReplyBox(button, messageContent, messageSender) {
    document.getElementById('inboxNewPopupWindow').style.display = "block";
    var contentInput = document.querySelector("[name=content]");
    if (contentInput) {
        contentInput.focus();
    }
    document.querySelector("[name=message_id]").value = button.getAttribute("data");
}

document.addEventListener("DOMContentLoaded", function () {
    "use strict";
    // Get the modal
    var modal = document.getElementById('inboxPopupWindow');

    // Get the <span> element that closes the modal
    var span = document.querySelector(".close");

    // When the user clicks on <span> (x), close the modal
    if (span) {
        span.onclick = function() {
            modal.style.display = "none";
        }
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Handle ESC key (key code 27)
    document.addEventListener('keyup', function(e) {
        if (e.keyCode == 27) {
            modal.style.display = "none";
        }
    });
}, true);

// Inbox toggle select all messags
function toggleSelectAll(button) {
    "use strict";

    var checkBoxes = document.querySelectorAll("#selectableCheckbox");

    if (button.innerHTML === "SELECT ALL") {
        button.innerHTML = "DE-SELECT ALL";
        checkBoxes.forEach(check);
    } else {
        button.innerHTML = "SELECT ALL";
        checkBoxes.forEach(uncheck);
    }

    function check(element) {
        element.checked = true;
    }

    function uncheck(element) {
        element.checked = false;
    }
}

// Inbox form data transfer
function getIdsFromCheckboxes(element) {
    "use strict";
    var form = document.forms[element.getAttribute("form")];
    var ids = [];
    var i;
    for (i = 0; i < form.length; i++) {
        if (form.elements[i].checked) {
            ids.push(form.elements[i].value);
        }
    }
    return {
        "action": element.getAttribute("name"),
        "ids": ids
    };
}

function updateMessageTable(xhttp, oldData) {
    "use strict";
    if (xhttp.responseText == "success") {
        var ids = oldData.ids;
        var box;
        var i;
        for (i=0; i < ids.length; i++) {
            box = document.getElementById("messageID-" + ids[i]);
            box.parentElement.removeChild(box)
        }
    }
}


/* Server communication v2
Usage:
    <form onsubmit="return sendToPy(event, updateMessageTable, getIdsFromCheckboxes);></form>
    OR
    <button onclick="sendToPy(event, someCallBack, somePreprocess, someUrl);"></button>

NOTE: Form must have a return method too.
NOTE: url defaults to current page if unspecified.
NOTE: if data is a string window location isn't passed.
If the data is (preferably) a JSON object the page location is passed along.
*/
function sendToPy(event, callback, cmd, data, preProcess, url) {
    "use strict";
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
                if (xhttp.getResponseHeader("Content-Type") === "application/json") {
                    var response = JSON.parse(xhttp.responseText);
                    callback(response, oldData)
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

// Get a valid function handler (if one exists) for a given function string.
// Probably no longer relevant now that I can pass function names directly.
function getFunc(element, funcName) {
    "use strict";
    func =  window[element.getAttribute(funcName)];
    if (func === undefined) {
        func = function () {
            return;
        };
    }
    return func;
}

// Basic print statement that should be built in!!!
function log (data) {
    "use strict";
    console.log(data);
}
