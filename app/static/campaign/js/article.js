function getArticle() {
	$.getJSON($SCRIPT_ROOT + '/article',
	function(data) {
		populateArticle(data);
	});
};

function populateArticle(data) {
	$('.article-snippet').remove();
	var html = '<div class="article-snippet"><a href="' + data['link'] + '"><h2>' + data['title'] + '</h2></a><h4>' + data['author'] + '</h4><p>' + data['journal'] + '</p></div>';
	$(html).hide().appendTo('#election-info').fadeIn('slow');
}