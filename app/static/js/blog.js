function masonry() {
	var masonry = new Masonry('#projects-grid', {
		itemSelector: '.project'
	});
	
	imagesLoaded('#projects-grid', function() {
		masonry.layout();
	});
}