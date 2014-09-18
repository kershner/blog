function hiddenMenu() {
	$(window).scroll(function() {
		if ($(window).scrollTop() > 655) {
			$("#hidden-menu").fadeIn('fast').css('display', 'block');
		}
		else if ($(window).scrollTop() < 656) {
			$("#hidden-menu").fadeOut('fast');
		}
	});
}