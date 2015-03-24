$(document).ready(function() {
	// Setting background color initially, calling changer function
	var color = randomColor();
	$('#content').animate({backgroundColor: color}, {queue: false, duration: 13});
	$('body').animate({backgroundColor: color}, {queue: false, duration: 13});
	setInterval(backgroundChange, 10000);
	
	// Function to disable pressing ENTER in the text field
	$('#delay').keypress(function(e){
    	if (e.keyCode == 13) {
        	return false;
	}});

	alterSesseion();
});

// Creating a global dictionary to be used in the on-click 'focus'
var options = {};
window.elements = [];
var elements_array = window.elements.slice();

// Automatic random background color changer
function backgroundChange() {
	var color = randomColor();
	var randomNumber = Math.floor(Math.random() * (6000 - 1000 + 1)) + 1000;
	$('#content').animate({backgroundColor: color}, {queue: false, duration: randomNumber});
	$('body').animate({backgroundColor: color}, {queue: false, duration: randomNumber});
}

// Function to click on GIF and 'focus' on it - animation stops,
// CSS height/width and Z index get larger.
// Another click sets them to normal
function focusClick(target) {
	$(target).toggle(function() {
		$(this).stop();
		var orig_height = 'height';
		var orig_width = 'width';
		options[orig_height] = $(this).css('height');
		options[orig_width] = $(this).css('width');
		$(this).stop(true, true).animate({ width: '+=50%', height: '+=50%' }, 'fast');
		$(this).css('z-index', 20);
		animateDiv($(this));
	}, function() {
		$(this).stop().animate(options, 'fast');
		$(this).css('z-index', 1);
		animateDiv($(this));
	});
}

// Function to pick a random element and 'focus' on it for a set
// amount of time
function focusGif() {
	// Pulling the GIF's original dimensions to revert back to when
	// 'unfocusing'.  'Pop'ing from an array to make sure an element
	// isn't focused on twice in a row, which could cause its dimensions to get
	// messed up over time.
	if (elements_array.length === 0) {
		elements_array = elements.slice();
	}
	var rand_gif = elements_array.pop();
	var orig_height = 'height';
	var orig_width = 'width';
	var options1 = {};
	options1[orig_height] = $(rand_gif).css('height');
	options1[orig_width] = $(rand_gif).css('width');
	$(rand_gif).stop(true, true).animate({ width: '+=50%', height: '+=50%' }, 'slow');
	$(rand_gif).css('z-index', 20);
	setTimeout(function() {
		$(rand_gif).stop(true, true).animate(options1, 'slow');
		$(rand_gif).css('z-index', 1);
	}, 10000);
}

// Making images draggable
function draggableImage() {
	$('img').draggable({
		start: function(event, ui) {
			$(this).stop();
		},
		stop: function(event, ui) {
			animateDiv($(this));
		}
	});
}

// The functions below define the animation of the images
function getStartPos($target) {
	var h = $("#content").height(); 
	var w = $("#content").width();
	$target.css({
		"top": (Math.random() * h) + 'px',
		"left": (Math.random() * w) + 'px'
	});
	$target.fadeIn(900);
}

function makeNewPosition($content) {
	// Get viewport dimensions (remove the dimension of the div)
	var h = $content.height() - 300;
	var w = $content.width() - 200;

	var nh = Math.floor(Math.random() * h);
	var nw = Math.floor(Math.random() * w);

	return [nh, nw];
}

function calcSpeed(prev, next) {
	var x = Math.abs(prev[1] - next[1]);
	var y = Math.abs(prev[0] - next[0]);
	var greatest = x > y ? x : y;
	var speedModifier = 0.1;
	var speed = Math.ceil(greatest / speedModifier);

	return speed;
}

function animateDiv($target) {
	var newq = makeNewPosition($target.parent());
	var oldq = $target.position();
	var speed = calcSpeed([oldq.top, oldq.left], newq);
	
	$target.animate({
		top: newq[0],
		left: newq[1]
	}, speed, function () {
		animateDiv($target);
	});
}

// Json Function to Retrieve Images from Server
function getImages() {
	$('img').fadeOut(2000);
	setTimeout($('img').remove(), 3000);
	clearInterval(window.delay);
	$.getJSON($SCRIPT_ROOT + '/gif_party_json', 
		function(data) {
            var delay = data.delay;
			var slider1_1 = $('#slider1-1').slider('option', 'value');
			var slider1_2 = $('#slider1-2').slider('option', 'value');
			var slider1_3 = $('#slider1-3').slider('option', 'value');
			var slider1_4 = $('#slider1-4').slider('option', 'value');
			var slider2 = $('#slider2').slider('option', 'value');
			var slider3 = $('#slider3').slider('option', 'value');
			var slider4 = $('#slider4').slider('option', 'value');
			
			window.elements = [];
			for (i = 0; i < data.number; i++) {
				$('<img src="' + data.URLs[i] + '"/>').addClass(String(i)).appendTo('#content');
				window.elements.push('.' + i );
			}

			for (i = 0; i < elements.length; i++) {
				getStartPos($(elements[i]));
				animateDiv($(elements[i]));
				focusClick($(elements[i]));
			}			
			window.delay = setInterval(getImages, delay);
			$('img').css({
				'border-top-left-radius': slider1_1 + '%',
				'border-top-right-radius': slider1_2 + '%',
				'border-bottom-left-radius': slider1_3 + '%',
				'border-bottom-right-radius': slider1_4 + '%',
				'min-width': slider2 + 'px',
				'min-height': slider2 + 'px',
				'max-width': slider3 + 'px',
				'max-height': slider3 + 'px'
			});
			draggableImage();
			getSettings();
		});
    return false;
}

// Functions to alter Flask session data via JSON
function alterSesseion() {
	// Number of GIFs selection
	$('#5').click(function() {
		$.getJSON($SCRIPT_ROOT + '/gif_party_json_5',
		function(data) {
			getImages();
		});
	});
	
	$('#10').click(function() {
		$.getJSON($SCRIPT_ROOT + '/gif_party_json_10',
		function(data) {
			getImages();
		});
	});
	
	$('#20').click(function() {
		$.getJSON($SCRIPT_ROOT + '/gif_party_json_20',
		function(data) {
			getImages();
		});
	});
	
	// Category Selection
	$('#all').click(function() {
		$.getJSON($SCRIPT_ROOT + '/gif_party_json_all',
		function(data) {
			getImages();
		});
	});
	
	$('#animals').click(function() {
		$.getJSON($SCRIPT_ROOT + '/gif_party_json_animals',
		function(data) {
			getImages();
		});
	});
	
	$('#gaming').click(function() {
		$.getJSON($SCRIPT_ROOT + '/gif_party_json_gaming',
		function(data) {
			getImages();
		});
	});
	
	$('#strange').click(function() {
		$.getJSON($SCRIPT_ROOT + '/gif_party_json_strange',
		function(data) {
			getImages();
		});
	});
	
	$('#educational').click(function() {
		$.getJSON($SCRIPT_ROOT + '/gif_party_json_educational',
		function(data) {
			getImages();
		});
	});
	
	// Auto Refresh
	$('#submit').click(function() {
		var data = $('#delay').val();
		$.ajax({
			type: 'POST',
			url: $SCRIPT_ROOT + '/gif_party_json_delay',
			data: JSON.stringify(data, null, '\t'),
			contentType: 'application/json;charset=UTF-8',
			success: function() {
				getImages();
			}
		});
	});
}

// Function to display the current settings
function getSettings() {
	$('.setting').remove();
	$.getJSON($SCRIPT_ROOT + '/gif_party_json',
		function(data) {
			var category = data.category;
			var number = data.number;
			var delay = data.delay;
			delay = String(delay).slice(0, 2);
			$('<p>' + category + '</p><br>').addClass('setting').appendTo('#settings-values');
			$('<p>' + number + '</p><br>').addClass('setting').appendTo('#settings-values');
			$('<p>' + delay + ' seconds</p><br>').addClass('setting').appendTo('#settings-values');
	});
}

// Sliders////////////////////////////////////////
// Border-radius sliders
function alterBorderRadiusTopLeft() {
	var slider = $('#slider1-1').slider('value');
	$('img').css('border-top-left-radius', slider + '%');
}

function alterBorderRadiusTopRight() {
	var slider = $('#slider1-2').slider('value');
	$('img').css('border-top-right-radius', slider + '%');
}

function alterBorderRadiusBottomLeft() {
	var slider = $('#slider1-3').slider('value');
	$('img').css('border-bottom-left-radius', slider + '%');
}

function alterBorderRadiusBottomRight() {
	var slider = $('#slider1-4').slider('value');
	$('img').css('border-bottom-right-radius', slider + '%');
}

$(function() {
	$('#slider1-1').slider({
		orientation: 'horizontal',
		range: 'min',
		max: 50,
		min: 5,
		value: 5,
		slide: alterBorderRadiusTopLeft,
		change: alterBorderRadiusTopLeft
	});
});

$(function() {
	$('#slider1-2').slider({
		orientation: 'horizontal',
		range: 'min',
		max: 50,
		min: 5,
		value: 5,
		slide: alterBorderRadiusTopRight,
		change: alterBorderRadiusTopRight
	});
});

$(function() {
	$('#slider1-3').slider({
		orientation: 'horizontal',
		range: 'min',
		max: 50,
		min: 5,
		value: 5,
		slide: alterBorderRadiusBottomLeft,
		change: alterBorderRadiusBottomLeft
	});
});

$(function() {
	$('#slider1-4').slider({
		orientation: 'horizontal',
		range: 'min',
		max: 50,
		min: 5,
		value: 5,
		slide: alterBorderRadiusBottomRight,
		change: alterBorderRadiusBottomRight
	});
});

// Min-size slider
function alterImageSize() {
	var slider = $('#slider2').slider('value');
	$('img').css('min-width', slider + 'px');
	$('img').css('min-height', slider + 'px');
}

$(function() {
	$('#slider2').slider({
		orientation: 'horizontal',
		range: 'min',
		step: 100,
		max: 500,
		value: 0,
		slide: alterImageSize,
		change: alterImageSize
	});
});

// Max-size slider
function alterImageSize1() {
	var slider = $('#slider3').slider('value');
	$('img').css('max-width', slider + 'px');
	$('img').css('max-height', slider + 'px');
}

$(function() {
	$('#slider3').slider({
		orientation: 'horizontal',
		range: 'min',
		step: 100,
		max: 500,
		min: 100,
		value: 500,
		slide: alterImageSize1,
		change: alterImageSize1
	});
});