// Hidden Menu Script
function hiddenMenu() {
	$(window).scroll(function() {
		if ($(window).scrollTop() > 793) {
			$("#hidden-menu").fadeIn('fast').css('display', 'block');
		}
		else if ($(window).scrollTop() < 794) {
			$("#hidden-menu").fadeOut('fast');
		}
	});
}

// Slogan script
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

// Article Script
function getArticle() {
	$.getJSON($SCRIPT_ROOT + '/article',
	function(data) {
		populateArticle(data);
	});
};

function populateArticle(data) {
	$('.article-snippet').remove();
	
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

function getArticle2() {
	$.getJSON($SCRIPT_ROOT + '/article2',
	function(data) {
		populateArticle2(data);
    });
};

function populateArticle2(data) {
	$('.article-snippet2').remove();
	
	if (data['length'] < 70) {
		var html = '<br><br><br><div class="article-snippet2"><a href="' + data['link'] + '"><h2>' + data['title'] + '</h2></a><p class="author">' + data['author'] + '</p><p>' + data['journal'] + '</p></div>';
	}
	else if (71 < data['length'] < 80) {
		var html = '<br><br><div class="article-snippet2"><a href="' + data['link'] + '"><h2>' + data['title'] + '</h2></a><p class="author">' + data['author'] + '</p><p>' + data['journal'] + '</p></div>';
	}
	else if (81 < data['length'] < 90) {
		var html = '<br><div class="article-snippet2"><a href="' + data['link'] + '"><h2>' + data['title'] + '</h2></a><p class="author">' + data['author'] + '</p><p>' + data['journal'] + '</p></div>';
	}
	else {
		var html = '<div class="article-snippet2"><a href="' + data['link'] + '"><h2>' + data['title'] + '</h2></a><p class="author">' + data['author'] + '</p><p>' + data['journal'] + '</p></div>';
	}
	
	var newDiv = '<div class="article-snippet2">' + html + '</div>'
	
	$(newDiv).hide().appendTo('#events').fadeIn('slow');
}