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
                        // Send the last element to check if we should show a
                        // notification.
//                        showGlobalNotificationButton(requestArray[requestArray.length-1]);
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

function refreshPage() {
    location.reload();
}

// Allows the user to switch between the register and login forms.
function toggleLoginRegister(button) {
    var tag = button.getAttribute('data');
    var registerForm = document.getElementById("register-form");
    var loginForm = document.getElementById("login-form");
    var resetForm = document.getElementById("reset-form");
    var errorDiv = document.getElementById("error");
    if (tag === "register") {
        registerForm.style.display = "block";
        loginForm.style.display = "none";
        resetForm.style.display = "none";
        errorDiv.style.display = "none";
        document.getElementById("registerFocus").focus();
    } else if (tag === "login") {
        registerForm.style.display = "none";
        loginForm.style.display = "block";
        resetForm.style.display = "none";
        errorDiv.style.display = "none";
        document.getElementById("loginFocus").focus();
    } else if (tag === "reset") {
        registerForm.style.display = "none";
        loginForm.style.display = "none";
        resetForm.style.display = "block";
        errorDiv.style.display = "none";
        document.getElementById("resetFocus").focus();
    }
}

function doNothing() { // This should be removed soon. I'm just not sure how to get SendToPy to not run any JS function.
    return;
}

function checkPasswordMatch() {
    var continueButton = document.getElementById("continueButton");
    var errorDiv = document.getElementById("error");
    var password = document.getElementById("password").value;
    var passwordCheck = document.getElementById("passwordCheck").value;

    if (password != passwordCheck) {
        errorDiv.innerHTML = "These passwords don't match!";
        continueButton.disabled = true;
        continueButton.style.background = "#5e9960";
    } else {
        errorDiv.innerHTML = "These passwords match.";
        continueButton.disabled = false;
        continueButton.style.background = "#4CAF50";
    }
}

function show(element) {
    element.classList.remove('hide')
    element.classList.add('show')
}

function hide(element) {
    element.classList.remove('show')
    element.classList.add('hide')
}

// Allow the sidebar to be sticky its top and bottom to the display window.
var lastYOffset = window.pageYOffset;
function stickyTopAndBottom() {
    "use strict";
    var newOffset = window.pageYOffset;
    var sidebarDiv = document.getElementById("sidebar");
    var minOffset = 10;
    var extraBottomSpacing = 5;  // compensates for bottom being too close.
    var maxOffset = sidebarDiv.scrollHeight - window.innerHeight + minOffset + extraBottomSpacing;
    var currentOffset = parseInt(window.getComputedStyle(sidebarDiv, "style").top.slice(0, -2));
    var scrollYDirection = (lastYOffset < newOffset
        ? "down"
        : "up");

    if (scrollYDirection === "down") {
        currentOffset = currentOffset - (newOffset - lastYOffset);
        if (currentOffset <= -maxOffset) {
            currentOffset = -maxOffset;
        }
    } else if (scrollYDirection === "up") {
        currentOffset = currentOffset + (lastYOffset - newOffset);
        if (currentOffset >= minOffset) {
            currentOffset = minOffset;
        }
    }

    sidebarDiv.style.top = currentOffset + "px";
    lastYOffset = newOffset;
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
function toggleEquip(response, oldData) {
    "use strict";
//    log("toggleEquip function");
//    log("Response:")
//    console.log(response);
//    log("oldData:")
//    console.log(oldData);
    // For readability.
    // tooltipDiv is the location of the specific item that is being moved.
    // inventoryItemDiv is the container that the item is in.
    // emptySlotDiv is the picture that is displayed in a given inventory slot
    // i.e. the head has an gray/gold helmet pic.
    var tooltipDiv;
    var inventoryItemDiv;
    var emptySlotDiv;
    var command;
    var primarySlotType;

    command = response.command;
    // primarySlotType is the location in the inventory that the item
    // will be equipped into.
    primarySlotType = response.primarySlotType;

    // When you are Unequipping an Item.
    if (command === "unequip") {
        tooltipDiv = document.getElementById("item-" + oldData.id);
        inventoryItemDiv = tooltipDiv.parentElement;
//        log("iventoryItemDiv.id: " + inventoryItemDiv.id)
        emptySlotDiv = document.getElementById(inventoryItemDiv.id + "-empty");
        unequip(tooltipDiv, inventoryItemDiv, emptySlotDiv, primarySlotType);

    // When you are Equipping and Item.
    } else if (command === "equip") {
        var slotDiv;
        var idsToUnequip;

        idsToUnequip = response.idsToUnequip;
        var itemId;
        var i;
        var idsLength = idsToUnequip.length
        for (i=0; i< idsLength; i++) {
            itemId = idsToUnequip[i];
//            log("id: " + itemId)
            tooltipDiv = document.getElementById("item-" + itemId)
            inventoryItemDiv = tooltipDiv.parentElement;
//            log("iventoryItemDiv.id: " + inventoryItemDiv.id)
            emptySlotDiv = document.getElementById(inventoryItemDiv.id + "-empty");
            unequip(tooltipDiv, inventoryItemDiv, emptySlotDiv, primarySlotType);
        }
        tooltipDiv = document.getElementById("item-" + oldData.id);
        equip(tooltipDiv, primarySlotType)
    }
}

// Equip a given item into the correct slot on the inventory diagram.
function equip(tooltipDiv, primarySlotType) {
    "use strict";
    var inventoryItemDiv;
    var slotDiv;
    var emptySlotDiv;
    var slotType;
    var rightHandDiv;
    var emptyLeftHandDiv;

    inventoryItemDiv = tooltipDiv.parentElement;
    slotDiv = document.getElementById("inventory-" + primarySlotType);
    emptySlotDiv = document.getElementById("inventory-" + primarySlotType + "-empty");

    // Delete the inventoryItemDiv
    // Hide the emptySlot Div.
    // Move the tooltipDiv
    inventoryItemDiv.parentElement.removeChild(inventoryItemDiv);
    emptySlotDiv.style.display = "none";
    slotDiv.appendChild(tooltipDiv);
    slotDiv.style.display = "";

    // Make the alternate overlapping slot invisible.
    if (primarySlotType === "both-hands") {
        slotType = "right-hand";
        rightHandDiv = document.getElementById("inventory-" + slotType);
        rightHandDiv.style.display = "none";
        slotType = "left-hand";
        emptyLeftHandDiv = document.getElementById("inventory-" + slotType + "-empty");
        emptyLeftHandDiv.src = tooltipDiv.firstElementChild.src;
//        log(tooltipDiv);
//        log(emptyLeftHandDiv);
//        log(emptyLeftHandDiv.src);
        emptyLeftHandDiv.style.filter = "grayscale(100%) opacity(50%)"
    } else if (["left-hand", "right-hand"].indexOf(primarySlotType) != -1) {
        slotType = "both-hands";
        slotDiv = document.getElementById("inventory-" + slotType);
        slotDiv.style.display = "none";
    }
}

// Unequip an item from its current location.
// Put it at the back of the inventory
function unequip(tooltipDiv, inventoryItemDiv, emptySlotDiv, primarySlotType) {
    "use strict";

    var unequippedItemDiv;
    var unequippedGeneralDiv;
    var emptyLeftHandDiv;
    var rightHandDiv;
    var bothHandsDiv;
    var slotType;

    // Reset left hand div.
    // Lame check if element is in array.
//    log("primary slot type unequip");
//    log(primarySlotType);
    if (["both-hands", "left-hand", "right-hand"].indexOf(primarySlotType) != -1) {
//        log("Should be reseting left-hand image!")
        slotType = "left-hand";
        emptyLeftHandDiv = document.getElementById("inventory-" + slotType + "-empty");
        emptyLeftHandDiv.src = "static/images/items/inventory_left_hand.jpg";
        emptyLeftHandDiv.style.filter = "";
        slotType = "right-hand";
        rightHandDiv = document.getElementById("inventory-" + slotType);
        rightHandDiv.style.display = "";
        slotType = "both-hands";
        bothHandsDiv = document.getElementById("inventory-" + slotType);
        bothHandsDiv.style.display = "none";
    }
    inventoryItemDiv.removeChild(tooltipDiv);
    emptySlotDiv.style.display = "inline";

    unequippedItemDiv = document.createElement("div");
    unequippedItemDiv.classList.add("inventory-unequipped", "inventory-item");
    unequippedItemDiv.appendChild(tooltipDiv);

    unequippedGeneralDiv = document.getElementById("unequipped");
    unequippedGeneralDiv.appendChild(unequippedItemDiv);
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

// I moved this function here instead of putting it at the bottom of each page which uses my accordion. BUT for some reason if I put it here
// it becomes glitchy. I need to click the element twice for it to work now. I need to solve it before I move them all here.
function genericAccordion(button) {
    button.classList.toggle("active");
    var panel = button.nextElementSibling;
    if (panel.style.display === "block") {
        panel.style.display = "none";
    } else {
        panel.style.display = "block";
    }
}

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

function proficiencyTooltip(response, oldData) {
    var newTooltip;
    newTooltip = document.getElementById("proficiencyTooltip");
    newTooltip.innerHTML = response.tooltip;
    if ("pointsRemaining" in response) {
        document.getElementById("pointsRemaining").innerHTML = response.pointsRemaining;
        document.getElementById("proficiency-" + oldData.id).innerHTML = response.level;
    }
}

function abilityTooltip(response, oldData) {
    var newTooltip;
    newTooltip = document.getElementById("abilityTooltip");
    newTooltip.innerHTML = response.tooltip;
    if ("pointsRemaining" in response) {
        document.getElementById("pointsRemaining").innerHTML = response.pointsRemaining;
        document.getElementById("ability-" + oldData.id).innerHTML = response.level;
    }
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
    var endImage = '.jpg" alt="none"  style="display:block;margin-left:auto;margin-right:auto;height:200px;width:200px;">';
    newTooltip = document.getElementById("abilityChoiceTooltip");
    newTooltip.innerHTML = description;
    newImage = document.getElementById("choiceImage");
    newImage.innerHTML = startImage + image + endImage;
}

function questTooltip(response, oldData) {
    "use strict";
    var newTooltip;
    var tooltipReward;

    newTooltip = document.getElementById("questTooltip");
    newTooltip.innerHTML = response.description;
    tooltipReward = document.getElementById("questReward");
    tooltipReward.innerHTML = "<h3>Your reward for completing this quest is: " + response.reward +"xp</h3>";
}

function pageReload(button) {
    location.reload();
}

// Show the global notification button
// This function handles the possibility of passing in invalid data.
// Returns the invalid data. Returns nothing if data is valid.
function showGlobalNotificationButton(isNotice, isJSON) {
    if (!isJSON && typeof isNotice === "string") {
        // It might be the right kind of data.
        if (isNotice.search("isNotice") === 0) {
            // Yay! The right kind of data!
            isNotice = isNotice.split('=')[1];
            isNotice = eval(isNotice);
        } else {
            // I guess it wasn't the right kind after all that ...
            return isNotice;
        }
    } else if (isJSON){
        ; // Good data! Continue to other code!
    } else {
        // if not JSON or string it definitely isn't the right kind of data.
        return isNotice;
    }

    if (isNotice) {
        button = document.getElementById("globalNotificationButton");
        button.style.visibility = "visible";
    }
    return null; // If this variable was a valid isNotice return nothing.
}

// Consider moving much of this to HTML?
function redirectUserFromNotification(response, oldData) {
    // Redirect the user to the appropriate page
    // Close the notification
    var clickedButton = document.getElementById("notice-" + oldData['id']);
    clickedButton.style.display = "none";
    if (response["redirect"] == "True") {
        window.location.href = response["url"]
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

function newThreadBox(button, threadName, threadDescription) {
    document.getElementById('newThreadPopupWindow').style.display = "block";
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

    if (modal) {
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
    }
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

function getFormData(form) {
    // Attempt to avoid using Form post and send the form data manually.
    // <form method="post" onsubmit="return sendToPy(event, updateFullPage, null, null, getFormData);">
//    log("Preprocessor for forms!")
//    log(form);
    var data = {"form": {}};
    var i;
    for (i=0; i < form.length; i++) {
        if (form.elements[i].name !== "") {
            data.form[form.elements[i].name] = form.elements[i].value;
        }
    }
    return data;
}

function updateFullPage(xhttp, oldData) {
    // Update the entire current page with a xhttp.response object.
    // e.g. return render_tempate('/home')
    // Would hard-write this page using passed data.
    // Probably a terrible idea.
//    log("Callback to updateFullPage!");
//    log(xhttp);
//    log(oldData);
    document.open();
    document.write(xhttp.response);
    document.close();
}

function redirect(xhttp, oldData) {
    // redirect the browser to the passed url.
    // e.g. return "/home" (in commands.py) would redirect to the home page.
//    log(xhttp.responseText);
    window.location.assign(xhttp.responseText);
}

// See https://stackoverflow.com/questions/1865837/whats-the-difference-between-window-location-and-window-location-replace#1865840
// This function will reload the current page AND prevent the user from
// going backwards to the current version of the page.
// NOTE: unless this page has extra handling ... there is nothing preventing
// the user from typing in the correct url.
function reloadReplaceURL(xhttp, oldData) {
    window.location.replace(oldData['location']);
}


/* Server communication v2
Usage:
    <form onsubmit="return sendToPy(
        event, updateMessageTable, null, null, getIdsFromCheckboxes);"></form>
    OR
    <button onclick="sendToPy(
        event, someCallBack, 'some_python_command_func', null,
        somePreprocess);"></button>

NOTE: Form must have a return method too.
NOTE: url defaults to current page if unspecified.
NOTE: if data is a string window location isn't passed.
If the data is (preferably) a JSON object the page location is passed along.
*/
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

// A preProcessor function to extract old style data from a clicked element
function getElementData(element) {
    return element.getAttribute('data');
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
