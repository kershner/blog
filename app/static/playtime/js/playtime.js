// Hidden Menu Script
function hiddenMenu() {
	$(window).scroll(function() {
		if ($(window).scrollTop() > 325) {
			$("#hidden-menu").fadeIn('fast').css('display', 'block');
		}
		else if ($(window).scrollTop() < 326) {
			$("#hidden-menu").fadeOut('fast');
		}
	});
}