function welcomeBlog() {
	blinkingArrow();
	waypoints();
	clickArrows();
	toTop();
	initSlick();
	sendEmail();
	grid();
	imageRotation();
	masonry();
}

// Called by blinkingArrow(), animates element's opacity
function checkOpacity(element) {
	var opacity = $(element).css('opacity');
	if (opacity === '0.5') {
		$(element).stop().animate({opacity: '1'}, 300);
	} else if (opacity === '1') {
		$(element).stop().animate({opacity: '0.5'}, 300);
	}
}

// Called by waypoints(), alters color of some HTML elements
function changeTheme(backgroundColor) {
	if (backgroundColor === '#FFC761') {
		var secondColor = '#1B4080';
	} else {
		var secondColor = '#FFC761';
	}

	$('html, body').css('background-color', backgroundColor);
	$('.welcome-header').css({'color': secondColor});
	$('#welcome-projects > hr').css({'background-color': secondColor});
	$('#welcome-contact > hr').css({'background-color': secondColor});
	$('#projects-blurb > span').css({'color': secondColor});
}

function blinkingArrow() {
	setInterval(function() {
		checkOpacity('#arrow');
		checkOpacity('#projects-arrow');
	}, 800);
}

// Calls changeTheme() when scrolled to certain divs
function waypoints() {
	// Scrolling up
	var welcomeMain = new Waypoint ({
		element: $('#arrow'),
		handler: function() {
			$('.up-arrow').stop().fadeOut(400);
			changeTheme('#00BFA5');
		},
		offset: 75
	});

	// Scrolling down
	var welcomeProjects = new Waypoint ({
		element: $('#arrow'),
		handler: function() {
			changeTheme('#FFC761');
			$('.up-arrow').stop().fadeIn(400);
		}, offset: 25
	});

	// Scrolling up
	var welcomeContact = new Waypoint ({
		element: $('#projects-arrow'),
		handler: function() {
			changeTheme('#FFC761');
		}, offset: 75
	});

	// Scrolling down
	var welcomeContact = new Waypoint ({
		element: $('#projects-arrow'),
		handler: function() {
			changeTheme('#386ECA');
		}, offset: 25
	});
}

// Controls fixed scrolling when nav arrows clicked
function clickArrows() {
	$('#arrow').on('click', function() {
		$('html, body').animate({
			scrollTop: $('#welcome-projects').offset().top
		}, 800);
	});

	$('#projects-arrow').on('click', function() {
		$('html, body').animate({
			scrollTop: $('#welcome-contact').offset().top
		}, 800);
	});
}

// Controls action when 'top' arrow is clicked
function toTop() {
	$('.up-arrow').on('click', function() {
		$(this).stop().fadeOut(400);
		$('html, body').stop().animate({
			scrollTop: $('#welcome-container').offset().top
		}, 600);
	});
}

// Initializes the slick.js image carousel
function initSlick() {
	$('.slick-images').slick({
		focusOnSelect: true,
		pauseOnHover: false,
		centerMode: true,
		centerPadding: '5px',
		slidesToShow: 4,
		slidesToScroll: 4,
		autoplay: true,
		autoplaySpeed: 8000,
		dots: true,
		nextArrow: '<i></i>',
		prevArrow: '<i></i>',
		lazyLoad: 'progressive',
		responsive: [
		{
			breakpoint: 1300,
			settings: {
			slidesToShow: 3,
			slidesToScroll: 3
		}
			},
		{
			breakpoint: 1000,
			settings: {
			slidesToShow: 2,
			slidesToScroll: 2
		}
			},
		{
			breakpoint: 700,
			settings: {
			slidesToShow: 1,
			slidesToScroll: 1
			}
		}
	  ]
	});
}

// Logic to control contact form
function sendEmail() {
	$('#submit').on('click', function() {
		var email = 'tylerkershner@gmail.com';
		var subject = $('#subject').val();
		var body = $('#body').val();
		if (subject.length < 1) {
			var message = 'Subject field is empty.';
			showNotification(message);
		} else if (body.length < 1) {
			var message = 'Body field is empty.';
			showNotification(message);
		} else {
			var mailtoLink = 'mailto:' + email + '?subject=' + subject + '&body=' + body;
			window.location.href = mailtoLink;
		}
	});
}

// Fades in div with error messages related to contact form
function showNotification(message) {
	$('#notification').empty();
	var html = '<span>' + message + '</span>'
	$('#notification').append(html);
	$('#notification').fadeIn('fast');
	setTimeout(function() {
		$('#notification').fadeOut('slow');
	}, 2000);
}

// Fades out carousel, fades in image grid when icon clicked
function grid() {
	var clicked = false;
	$('#grid-select').on('click', function() {
		if (clicked) {
			clicked = false;
			$('#projects-grid').animate({'opacity': '0.0', 'z-index': '1'}, {
				duration: 100,
				easing: 'linear',
				complete: function() {
					$('#welcome-projects-carousel').stop().animate({'opacity': '1.0', 'z-index': '2'}, 400, 'linear');
				}
			});
			$(this).removeClass('grid-selected');
		} else {
			clicked = true;
			$('#welcome-projects-carousel').animate({'opacity': '0.0', 'z-index': '1'}, {
				duration: 100,
				easing: 'linear', 
				complete: function() {
					$('#projects-grid').animate({'opacity': '1.0', 'z-index': '2'}, 400, 'linear');
				}
			});
			$(this).addClass('grid-selected');
		}
	});
}

// Controls loading in/out of images for main image circle
function imageRotation() {
	var counter = 0;
	var images = [
		'http://www.kershner.org/static/images/bacon1.jpg',
		'http://www.kershner.org/static/images/bacon3.jpg',
		'http://www.kershner.org/static/images/bacon4.jpg'
	];

	setInterval(function() {
		if (counter >= images.length) {
			counter = 0;
		} else {
			swapImage(images[counter]);
			counter += 1
		}
	}, 8000);
}

// Called by imageRotation()
function swapImage(url) {
	$('#welcome-picture').fadeOut(600, 'linear', function() {
		$(this).remove();
		var html = '<img style="display: none;" id="welcome-picture" src="' + url + '">';
		$('#welcome-main > .image-wrapper').append(html);
		$('#welcome-picture').fadeIn(600, 'linear');
	});
}

// Initializes masonry grid
function masonry() {
	$('#projects-grid').masonry({
		itemSelector: '.project-grid',
		isFitWidth: true
	});
}