
$(document).ready(function(){
function mainfunction(){

}


	var file = document.getElementById('csv-file').files[0];



 
	$("#process-file").click(function(){
		var file = document.getElementById('csv-file').files[0];

		data = Papa.parse(file, {
				worker: false,
				header:true,
				complete: function(results) {

				// draw page after upload here
				json = results.data;
				var keys = Object.keys(json[0]);
				$('#id_Json').val(JSON.stringify(json))
		
				$("#process-file").css("visibility","hidden"); 
				$("#key_select").css("visibility","visible"); 
				
				for (each in keys){
				var string1 = "<option>" 
				var string2 =keys[each]
				var string3 ="</option>"			 
				$(".select_column").append(string1 + string2+ string3)
						}











											}
							}); 
			  
	});
//set the value of the street address submission to the same as the dropdown
$( "#street_address" ).change(function() {
  var street_address = $( "#street_address" ).val()
  console.log(street_address)
  $('textarea#id_street_column').val(street_address)
});

//set the value of the Suburb submission to the same as the dropdown
$( "#suburb" ).change(function() {
  var suburb = $( "#suburb" ).val()
  console.log(suburb)
  $('textarea#id_suburb_column').val(suburb)
});

//set the value of the State submission to the same as the dropdown
$( "#state" ).change(function() {
  var state = $( "#state" ).val()
  console.log(state)
  $('textarea#id_state_column').val(state)
});

//set the value of the postcode submission to the same as the dropdown
$( "#postcode" ).change(function() {
  var postcode = $( "#postcode" ).val()
  console.log(postcode)
  $('textarea#id_postcode_column').val(postcode)
});




});
