
// This is for the quest pop-up window. When the user clicks on div, open/close the popup
function quest_popup() {
    var popup = document.getElementById('js_popupachievement');
    popup.classList.toggle('show');
}

// Only run what comes next *after* the page has loaded
addEventListener("DOMContentLoaded", function() {
  // Grab all of the elements with a class of command
  // (which all of the buttons we just created have)
  var commandButtons = document.querySelectorAll(".command");
  for (var i=0, l=commandButtons.length; i<l; i++) {
    var button = commandButtons[i];
    // For each button, listen for the "click" event
    button.addEventListener("click", function(e) {
      // When a click happens, stop the button
      // from submitting our form (if we have one)
      e.preventDefault();

      var clickedButton = e.target;
      var command = clickedButton.value;

      // Now we need to send the data to our server
      // without reloading the page - this is the domain of
      // AJAX (Asynchronous JavaScript And XML)
      // We will create a new request object
      // and set up a handler for the response
      var request = new XMLHttpRequest();
      // We point the request at the appropriate command
      request.open("GET", "/" + command, true);
      // and then we send it off
      request.send();
	  location.reload();
	  
    });
  }
  
}, true);