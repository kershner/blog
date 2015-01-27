function blog() {
	smallMenu();
}

function projectsMasonry() {
	var masonry = new Masonry('#projects-grid', {
		itemSelector: '.project'
	});	
	imagesLoaded('#projects-grid', function() {
		masonry.layout();
	});
}

function smallMenu() {
	$(document).scroll(function() {
		var scrollTop = $(document).scrollTop();
		if (scrollTop > 150) {
			// Fade in small navbar
			var offset = scrollTop - 150
			$('.small-logo-container').fadeIn('fast');
		} else {
			$('.small-logo-container').fadeOut('fast');
		}
	});	
}