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

// This is for the quest pop-up window. When the user clicks on div, open/close the popup
function quest_popup() {
    var popup = document.getElementById('js_popupachievement');
    popup.classList.toggle('show');
}

function show(element) {
    element.classList.remove('hide')
    element.classList.add('show')
}

function hide(element) {
    element.classList.remove('show')
    element.classList.add('hide')
}

function archetype_popup(archetype) {
    var brute_popup = document.getElementById('js_popupbrute');
    var scoundrel_popup = document.getElementById('js_popupscoundrel');
    var ascetic_popup = document.getElementById('js_popupascetic');
    var survivalist_popup = document.getElementById('js_popupsurvivalist');
    var philosopher_popup = document.getElementById('js_popupphilosopher');
    var opportunist_popup = document.getElementById('js_popupopportunist');

    hide(brute_popup)
    hide(scoundrel_popup)
    hide(ascetic_popup)
    hide(survivalist_popup)
    hide(philosopher_popup)
    hide(opportunist_popup)

    if (archetype === 'brute') {
    show(brute_popup)
    } else if (archetype === 'scoundrel') {
    show(scoundrel_popup)
    } else if (archetype === 'ascetic') {
    show(ascetic_popup)
    } else if (archetype === 'survivalist') {
    show(survivalist_popup)
    } else if (archetype === 'philosopher') {
    show(philosopher_popup)
    } else if (archetype === 'opportunist') {
    show(opportunist_popup)
    }
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

// This function is used in the profile_proficiencies.html
// This function only runs if command code return successfully from Python.
// Could be updated to just rerender all html for tooltip :P
function updateProf(button, status, newTooltip) {
    "use strict";

    var id = 0;
    var i = 0;
    var heroProfPointsDiv = {};
    var profCurrentLvDiv = {};
    var tooltipPopupSpan = {};
    var buttonsNodeList = {};
    var errorDivNodeList = {};

    id = button.getAttribute("data");
    profCurrentLvDiv = document.getElementById("proficiency-" + id);
    heroProfPointsDiv = document.getElementById("points_remaining");
    tooltipPopupSpan = document.getElementById("tooltipPopup-" + id);

    profCurrentLvDiv.innerHTML = parseInt(profCurrentLvDiv.innerHTML) + 1;
    heroProfPointsDiv.innerHTML = parseInt(heroProfPointsDiv.innerHTML) - 1;
    tooltipPopupSpan.innerHTML = newTooltip;

    //hide this button
    if (status === "hide_this") {
        button.style.display = "none";
    //hide all buttons
    //show all errors
    } else if (status === "hide_all") {
        buttonsNodeList = document.querySelectorAll("button[id=proficiencyButton]");
        errorDivNodeList = document.querySelectorAll("div[id^=error-]");
        for (i = 0; i < buttonsNodeList.length; i += 1) {
            buttonsNodeList[i].style.display = "none";
            errorDivNodeList[i].style.display = "inline";
        }
    }
}

function updateAbility(button, id, ability_level, max_level, tree, description) {
    "use strict";

    var heroAbilityCurrentLvDiv = {};
    var heroBasicPointsDiv = {};
    var heroArchetypePointsDiv = {};
    var abilityDescriptionDiv = {};

    abilityDescriptionDiv = document.getElementById("ability-" + id + "-description");
    heroAbilityCurrentLvDiv = document.getElementById("ability-" + id);
    if (tree === "basic") {
        heroBasicPointsDiv = document.getElementById("basic_points_remaining");
        heroBasicPointsDiv.innerHTML = parseInt(heroBasicPointsDiv.innerHTML) - 1;
    } else if (tree === "archetype") {
        heroArchetypePointsDiv = document.getElementById("archetype_points_remaining");
        heroArchetypePointsDiv.innerHTML = parseInt(heroArchetypePointsDiv.innerHTML) - 1;
    }
    heroAbilityCurrentLvDiv.innerHTML = parseInt(heroAbilityCurrentLvDiv.innerHTML) + 1;
    abilityDescriptionDiv.innerHTML = description;
    //if parseInt(heroAbilityCurrentLvDiv.innerHTML) === max_level:
    //    gray it out



    if (status === "no ability points") {
    // make all buttons grayed out
    }
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
    document.getElementById('inboxPopupWindow').style.display = "block";

    var contentInput = document.querySelector("[name=content]");

    if (contentInput) {
        contentInput.focus();
    }
    document.getElementById('replyBoxMessageContent').innerHTML = messageContent;
    document.getElementById('replyBoxMessageSender').innerHTML = messageSender;
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

// Inbox form data transfer
function getIdsFromCheckboxes(element, event) {
    console.log("preprocessing data");
//    console.log(event);
//    console.log(element);
    return {"action": event.explicitOriginalTarget.getAttribute('name')}
}

function updateMessageTable(response) {
    console.log("Callback working");
    console.log("Response was: " + response.responseText);
}



/* Server communication v2
Usage:
    <form onsubmit="return sendToPy(event, updateMessageTable, getIdsFromCheckboxes);></form>
    OR
    <button onclick="sendToPy(event, someCallBack, somePreprocess, someUrl);"></button>

NOTE: Form must have a return method too.
NOTE: url defaults to current page unless specified.
*/
function sendToPy(event, callback, pre_process, url) {
    "use strict";
    var element = event.target;
    var data;

    if (!url) { // if url is blank use url of page
        url = window.location.pathname;
    }

    // Normal data processing is object form.
    // auto-converts to JSON.
    if (pre_process) {
        data = pre_process(element, event);
    } else {
        data = element.getAttribute('data');
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
function postJSON(url, data, callback) {
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (callback) {
                callback(this);
            }
        }
    };
    xhttp.open("POST", url, true);
    data = JSON.stringify(data);
    console.log("Data to be sent: " + data);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(data);
}

// Get a valid function handler (if one exists) for a given function string.
function getFunc(element, funcName) {
    func =  window[element.getAttribute(funcName)];
    if (func === undefined) {
        func = function () {
            return;
        };
    }
    return func;
}
