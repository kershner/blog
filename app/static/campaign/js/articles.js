function getArticle() {
	$.getJSON($SCRIPT_ROOT + '/article',
	function(data) {
		populateArticle(data);
	});
};

function populateArticle(data) {
	$('.article-snippet').remove();
	
	console.log(data['length']);
	
	if (data['length'] < 70) {
		var html = '<br><br><br><div class="article-snippet"><a href="' + data['link'] + '"><h2>' + data['title'] + '</h2></a><p class="author">' + data['author'] + '</p><p>' + data['journal'] + '</p></div>';
	}
	else if (71 < data['length'] < 80) {
		var html = '<br><br><div class="article-snippet"><a href="' + data['link'] + '"><h2>' + data['title'] + '</h2></a><p class="author">' + data['author'] + '</p><p>' + data['journal'] + '</p></div>';
	}
	else if (81 < data['length'] < 90) {
		var html = '<br><div class="article-snippet"><a href="' + data['link'] + '"><h2>' + data['title'] + '</h2></a><p class="author">' + data['author'] + '</p><p>' + data['journal'] + '</p></div>';
	}
	else {
		var html = '<div class="article-snippet"><a href="' + data['link'] + '"><h2>' + data['title'] + '</h2></a><p class="author">' + data['author'] + '</p><p>' + data['journal'] + '</p></div>';
	}
	
	var newDiv = '<div class="article-snippet">' + html + '</div>'
	
	$(newDiv).hide().appendTo('#election-info').fadeIn('slow');
};