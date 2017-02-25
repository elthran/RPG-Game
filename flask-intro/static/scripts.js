
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
