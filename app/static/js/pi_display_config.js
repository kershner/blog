function piDisplayConfig() {
	showSettings();
	clickUpdateGif();
	autoUpdate();
	prevGif();
	categorySelect();
	setDelay();
	showPrevious();
	prev5();
	theaterButton();
}

function showNotification(message) {
	var html = '<span>' + message + '</span>';
	$('#notification').empty();
	$('#notification').fadeIn(100);			
	$('#notification').append(html);
	setTimeout(fadeNotification, 2000)
}

function fadeNotification() {
	$('#notification').fadeOut('slow');
}

function updateGif() {
	console.log('Updating GIF...');
	$('#dynamic-image').remove();
	$.getJSON($SCRIPT_ROOT + '/pi-display-config-update', {
	}, function(data) {
		var html = '<img style="display:none;" id="img" src="' + data['current_gif'] + '">';		
		$('#image img').fadeOut('fast');
		$('#image').append(html);
		$('#img').fadeIn('slow');
		$('#img').imgCentering();
		showNotification(data['message']);
	});
	return false;
}

function buttonSelect(idName) {
	var buttons = ['#all', '#animals', '#gaming', '#strange', '#educational'];
	for (i = 0; i < buttons.length; i++) {
		$(buttons[i]).removeClass('button-selected');
	}
	$(idName).addClass('button-selected');
}

function categoryAjax(selection) {
	$.getJSON($SCRIPT_ROOT + '/pi-display-config-categories', {
		category: selection
	}, function(data) {
		showNotification(data['message']);
		updateCurrentSettings(data['category'], data['delay']);
	});
	return false;
}

function updateCurrentSettings(category, delay) {
	$('#current-settings').empty();
	var html = '<span>' + category + '</span><span>' + delay + ' seconds</span>';
	$('#current-settings').append(html);
}

function populateImages() {
	$('#last-played').fadeIn('fast');
	$.getJSON($SCRIPT_ROOT + '/previous-gifs', {
	}, function(data) {
		var html = '<div style="display: none;" id="' + data['id'] + '" class="last-played-images"></div>';
		$('#last-played').append(html);
		for (var i = 0; i < data['prev_5'].length; i++) {
			var image = '<img src="' + data['prev_5'][i] + '" class="animate">';
			$('#' + data['id']).append(image);
		};
		$('#' + data['id']).fadeIn('slow');
		clickImage();
	});
	return false;
}

function theaterMode() {
	$('body').css('background-image', 'none');
	$('body').css('background-color', '#000');
	$('#image').css({
		'width': 1024,
		'height': 768,
		'margin-left': '-=192px'
	});
	$('#dynamic-image').css({
		'width': 1024,
		'height': 768,
	});

	$('#title').css('margin-top', '-=125px');
	$("#image img").imgCentering();
	$("#dynamic-image img").imgCentering();
}

function removeTheater() {
	$('body').css('background-color', '#FFF');
	$('body').css('background-image', 'url(../static/images/pi_display_config/swirl_pattern.png)');
	$('#image').css({
		'width': 640,
		'height': 480,
		'margin-left': '+=192px'
	});

	$('#dynamic-image').css({
		'width': 640,
		'height': 480,
	});

	$('#title').css('margin-top', '+=125px');
	$("#image img").imgCentering();
	$("#dynamic-image img").imgCentering();
}

// Functions bound to HTML elements via click
function showSettings() {
	$('#settings-button').on('click', function() {
		$('#settings').fadeIn('fast');
	});
	$('#settings-close').on('click', function() {
		$('#settings').fadeOut('fast');
	});
}

function clickUpdateGif() {
	$('#update-gif').on('click', function() {
		updateGif();
	});
}

function autoUpdate() {
	var clicked = false;
	$('#auto-update').on('click', function() {
		if (clicked) {
			clearInterval(window.delay);			
			clicked = false;
			$(this).removeClass('selected');
			var message = 'Auto Update Off';
		    showNotification(message);
		} else {
			clearInterval(window.delay);
			clicked = true;
			$(this).addClass('selected');
			$.getJSON($SCRIPT_ROOT + '/pi-display-config-auto', function(data) {
		        delay = data['delay'];
		        window.delay = setInterval(updateGif, delay);
		        var message = 'Auto Update On';
		        showNotification(message);
		    });
		    return false
		}
	});
}

function prevGif() {
	$('#prev-gif').on('click', function() {
		$.getJSON($SCRIPT_ROOT + '/pi-display-config-prev', {
		}, function(data) {
			var html = '<img style="display: none;" id="dynamic-image" src="' + data['last_played'] + '">';
			$('#image img').remove();
			$('#dynamic-image').remove();
			$('#image').append(html);
			$("#dynamic-image").fadeIn('slow');
			$("#dynamic-image img").imgCentering();
			showNotification(data['message']);
		});
		return false;
	});
}

function categorySelect() {
	$('#all').on('click', function() {
		var selection = 'all';
		categoryAjax(selection);
		buttonSelect('#all');
	});
	$('#animals').on('click', function() {
		var selection = 'animals';
		categoryAjax(selection);
		buttonSelect('#animals');
	});
	$('#gaming').on('click', function() {
		var selection = 'gaming';
		categoryAjax(selection);
		buttonSelect('#gaming');
	});
	$('#strange').on('click', function() {
		var selection = 'strange';
		categoryAjax(selection);
		buttonSelect('#strange');
	});
	$('#educational').on('click', function() {
		var selection = 'educational';
		categoryAjax(selection);
		buttonSelect('#educational');
	});
}

function setDelay() {
	$('#submit').on('click', function() {
	    var delay = $('#delay').val();
	    if (delay >= 5) {
		    $.getJSON($SCRIPT_ROOT + '/pi-display-config-delay', {
				delay: delay
			}, function(data) {
				showNotification(data['message']);
				$('#delay').val('');
				updateCurrentSettings(data['category'], data['delay']);
			});
			return false;
		} else {
			message = 'Delay must be at least 5 seconds';
			showNotification(message);
		}
	});
}

function showPrevious() {
	var clicked = false;
	$('#previous-button').on('click', function() {		
		if (clicked) {
			clicked = false;
			closePrevious();
			$(this).removeClass('button-selected');
			$('#title').css('margin-top', '+=50px');		
	} else {
		clicked = true;
		$(this).addClass('button-selected');
		$('#title').css('margin-top', '-=50px');
		$('#last-played').fadeIn('fast');
		populateImages();
		}
	});
}

function closePrevious() {
	$('#previous-button').removeClass('button-selected');
	$('#last-played').fadeOut('fast');
	$.getJSON($SCRIPT_ROOT + '/clear-session', {
	}, function(data) {
		console.log(data['message']);
		$('.last-played-images').remove();
	});
	return false;
}

function prev5() {
	$('#prev-5-gifs').on('click', function() {
		populateImages();
	});
}

function theaterButton() {
	var clicked = false;
	$('#theater-button').on('click', function() {
		if (clicked) {
			clicked = false;
			$(this).removeClass('button-selected');
			removeTheater();
			$('#title').css('display', 'block');
			$("#dynamic-image img").imgCentering();
		} else {
			clicked = true;
			$(this).addClass('button-selected');
			$('#title').css('display', 'none');			
			theaterMode();
			$("#dynamic-image img").imgCentering();
		}
	});
}

////////////////////////////////////
function clickImage() {
	$('#last-played img').on('click', function() {
		$('#dynamic-image').remove();
		url = $(this)[0].src;
		var html = '<div id="dynamic-image"><img src="' + url + '"></div>';
		$('#image img').remove();
		$('#image').prepend(html);
		$('#dynamic-image').fadeIn('slow');
		setTimeout(function() {
			$('#dynamic-image img').imgCentering();
			console.log('Hello');
		}, 1000);		
	});
}