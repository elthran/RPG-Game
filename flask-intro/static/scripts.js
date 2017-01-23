  function strength_updater(AR) 
  {
    document.querySelector('#strength_output').value = AR;
    var select_strength = document.querySelector('#strength_output').value
    console.log(select_strength);
    
}

  function agility_updater(AR) 
  {
    document.querySelector('#agility_output').value = AR;
    var select_agility = document.querySelector('#agility_output').value
    console.log(select_agility);
    }


  function findTotal()
  {
    var arr = document.getElementsByName('Attributes');
    var tot={{ myHero.attribute_points }};
    
       for(var i=0;i<arr.length;i++){
        if(parseInt(arr[i].value))
            tot -= parseInt(arr[i].value);
    }

  document.getElementById('total_points_spent').value = tot;
	sumerror()
}


function sumerror()
  {
    var sum = document.getElementById('total_points_spent').value;
	
	if (sum < 0) 
  {
    document.getElementById('sumerror').value = '          You do not have enough points';
	}
  else {

		document.getElementById('sumerror').value = '';
	}
	

}
