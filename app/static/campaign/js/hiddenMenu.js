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