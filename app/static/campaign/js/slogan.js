function getData() {	
	$.getJSON($SCRIPT_ROOT + '/slogan',
	function(data) {
		populateSlogan(data);
	});
};

function populateSlogan(data) {
	$('.prepended').remove();
	var html = '<h2 class="prepended green">' + data['variable'] + '</h2>';
	$(html).hide().appendTo('#slogan').fadeIn('slow');
}