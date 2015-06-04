// Rutherford Community Pool Site Mockup
// June 2015

function smallMenu() {
	$('#hamburger').on('click', function() {
		$(this).css('color', '#5ab4ff');
		$('#small-nav-menu').css('display', 'block');
		smallMenuAbout();
		smallMenuServices();
		smallMenuSchedule();		
		$(this).on('click', function() {
			$(this).css('color', 'white');
			$('#small-nav-menu').css('display', 'none');
			smallMenu();
		});
	});
}

function smallMenuAbout() {
	$('#about-menu-small').on('click', function() {		
		$('#about-submenu-small').css('display', 'block');
		$('#about-menu-small .small-menu-select').addClass('small-menu-selected');
		$(this).on('click', function() {
			$('#about-submenu-small').css('display', 'none');
			$('#about-menu-small .small-menu-select').removeClass('small-menu-selected');
			smallMenuAbout();
		});		
	});
}

function smallMenuServices() {
	$('#services-menu-small').on('click', function() {
		$('#services-menu-small .small-menu-select').addClass('small-menu-selected');
		$('#services-submenu-small').css('display', 'block');
		$(this).on('click', function() {
			$('#services-menu-small .small-menu-select').removeClass('small-menu-selected');
			$('#services-submenu-small').css('display', 'none');
			smallMenuServices();
		});
	});
}

function smallMenuSchedule() {
	$('#schedule-menu-small').on('click', function() {
		$('#schedule-menu-small .small-menu-select').addClass('small-menu-selected');
		$('#schedule-submenu-small').css('display', 'block');
		$(this).on('click', function() {
			$('#schedule-menu-small .small-menu-select').removeClass('small-menu-selected');
			$('#schedule-submenu-small').css('display', 'none');
			smallMenuSchedule();
		});
	});
}

function loadBanners() {
	for (i = 2; i < 6; i ++) {
		var html = '<img src="/static/pool/images/pool-banner' + i + '.jpg" class="added-image banner' + i + '">';
		$('#banner-image').append(html);
	}
	setTimeout(function() {
		cycleBanners();
	}, 1000);
}

function cycleBanners() {
	var index = 1;
	setInterval(function() {
		if (index === 5) {
			index = 1;
			$('#banner-image').children('img').each(function() {
				$(this).addClass('banner-deselected');
				$(this).removeClass('banner-selected');
			});
		} else {
			index ++;
		}
		var element = '.banner' + index;
		$(element).removeClass('banner-deselected');
		$(element).addClass('banner-selected');
	}, 4000);
}
smallMenu();
loadBanners();