// Creating a global dictionary to be used in the on-click 'focus'
// function (directly below).  I will refactor this at some point when I understand
// JavaScript better
var options = {};
window.elements = [];
elements_array = window.elements.slice();

// Setting the initial background color
$(document).ready(function() {
	$('body').css('background-color', 'rgb(255, 255, 138)');
	$('content').css('background-color', 'rgb(255, 255, 138)');
});

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
};

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
};

// Functions to control the border-radius sliders
function alterBorderRadiusTopLeft() {
	var slider = $('#slider1-1').slider('value');
	$('img').css('border-top-left-radius', slider + '%');
};

function alterBorderRadiusTopRight() {
	var slider = $('#slider1-2').slider('value');
	$('img').css('border-top-right-radius', slider + '%');
};

function alterBorderRadiusBottomLeft() {
	var slider = $('#slider1-3').slider('value');
	$('img').css('border-bottom-left-radius', slider + '%');
};

function alterBorderRadiusBottomRight() {
	var slider = $('#slider1-4').slider('value');
	$('img').css('border-bottom-right-radius', slider + '%');
};

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

// Functions to control the min-size/max-size slider
function alterImageSize() {
	var slider = $('#slider2').slider('value');
	$('img').css('min-width', slider + 'px');
	$('img').css('min-height', slider + 'px');
};

$(function() {
	$('#slider2').slider({
	  orientation: 'horizontal',
	  range: 'min',
	  step: 100,
	  max: 400,
	  value: 0,
	  slide: alterImageSize,
	  change: alterImageSize
	});
});

function alterImageSize1() {
	var slider = $('#slider3').slider('value');
	$('img').css('max-width', slider + 'px');
	$('img').css('max-height', slider + 'px');
};

$(function() {
	$('#slider3').slider({
	  orientation: 'horizontal',
	  range: 'min',
	  step: 100,
	  max: 400,
	  min: 100,
	  value: 400,
	  slide: alterImageSize1,
	  change: alterImageSize1
	});
});

// Sliders to change background color
// Code basically lifted wholesale from the jQuery UI tutorial
function hexFromRGB(r, g, b) {
    var hex = [
      r.toString( 16 ),
      g.toString( 16 ),
      b.toString( 16 )
    ];
    $.each( hex, function( nr, val ) {
      if ( val.length === 1 ) {
        hex[ nr ] = "0" + val;
      }
    });
    return hex.join( "" ).toUpperCase();
}

function refreshSwatch() {
    var red = $( "#background-red" ).slider( "value" ),
      green = $( "#background-green" ).slider( "value" ),
      blue = $( "#background-blue" ).slider( "value" ),
      hex = hexFromRGB( red, green, blue );
    $( "body" ).css( "background-color", "#" + hex );
	$( "#content" ).css( "background-color", "#" + hex );
}
  
$(function() {
    $( "#background-red, #background-green, #background-blue" ).slider({
      orientation: "horizontal",
      range: "min",
      max: 255,
      value: 255,
      slide: refreshSwatch,
      change: refreshSwatch
    });
});

// Functions to control the box-shadow slider
function alterBoxShadow() {
	var slider = $('#slider4').slider('value');
	$('img').css('box-shadow', slider + 'px ' + slider + 'px ' + slider + 'px #000');
};

$(function() {
	$('#slider4').slider({
	  orientation: 'horizontal',
	  range: 'min',
	  max: 10,
	  value: 0,
	  slide: alterBoxShadow,
	  change: alterBoxShadow
	});
});

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

// The functions below define the animation of the images
function makeNewPosition($content) {

    // Get viewport dimensions (remove the dimension of the div)
    var h = $content.height() - 200;
    var w = $content.width() - 200;

    var nh = Math.floor(Math.random() * h);
    var nw = Math.floor(Math.random() * w);

    return [nh, nw];
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

function calcSpeed(prev, next) {

    var x = Math.abs(prev[1] - next[1]);
    var y = Math.abs(prev[0] - next[0]);

    var greatest = x > y ? x : y;

    var speedModifier = 0.1;

    var speed = Math.ceil(greatest / speedModifier);

    return speed;
}

// Json Function to Retrieve Images from Server
function getImages() {
    clearInterval(window.delay);
	$('img').remove();
    $.getJSON($SCRIPT_ROOT + '/gif_party_json', 
		function(data) {
            var delay = data['delay'];
			var slider1_1 = $('#slider1-1').slider('option', 'value');
			var slider1_2 = $('#slider1-2').slider('option', 'value');
			var slider1_3 = $('#slider1-3').slider('option', 'value');
			var slider1_4 = $('#slider1-4').slider('option', 'value');
			var slider2 = $('#slider2').slider('option', 'value');
			var slider3 = $('#slider3').slider('option', 'value');
			var slider4 = $('#slider4').slider('option', 'value');
			
			if ((data['number']) === 5) {
                url1 = data['URLs'][0];
                url2 = data['URLs'][1];
                url3 = data['URLs'][2];
                url4 = data['URLs'][3];
                url5 = data['URLs'][4];
                $('<img src="' + url1 + '"/>').addClass('a').appendTo('#content');
                $('<img src="' + url2 + '"/>').addClass('b').appendTo('#content');
                $('<img src="' + url3 + '"/>').addClass('c').appendTo('#content');
                $('<img src="' + url4 + '"/>').addClass('d').appendTo('#content');
                $('<img src="' + url5 + '"/>').addClass('e').appendTo('#content');
				window.elements = ['.a','.b','.c','.d','.e'];
            }
            else if ((data['number']) === 10) {
                url1 = data['URLs'][0];
                url2 = data['URLs'][1];
                url3 = data['URLs'][2];
                url4 = data['URLs'][3];
                url5 = data['URLs'][4];
                url6 = data['URLs'][5];
                url7 = data['URLs'][6];
                url8 = data['URLs'][7];
                url9 = data['URLs'][8];
                url10 = data['URLs'][9];
				$('<img src="' + url1 + '"/>').addClass('a').appendTo('#content');
                $('<img src="' + url2 + '"/>').addClass('b').appendTo('#content');
                $('<img src="' + url3 + '"/>').addClass('c').appendTo('#content');
                $('<img src="' + url4 + '"/>').addClass('d').appendTo('#content');
                $('<img src="' + url5 + '"/>').addClass('e').appendTo('#content');
				$('<img src="' + url6 + '"/>').addClass('f').appendTo('#content');
                $('<img src="' + url7 + '"/>').addClass('g').appendTo('#content');
                $('<img src="' + url8 + '"/>').addClass('h').appendTo('#content');
                $('<img src="' + url9 + '"/>').addClass('i').appendTo('#content');
                $('<img src="' + url10 + '"/>').addClass('j').appendTo('#content');
				window.elements = ['.a','.b','.c','.d','.e','.f','.g','.h','.i','.j'];
            }
            else if ((data['number']) === 20) {
                url1 = data['URLs'][0];
                url2 = data['URLs'][1];
                url3 = data['URLs'][2];
                url4 = data['URLs'][3];
                url5 = data['URLs'][4];
                url6 = data['URLs'][5];
                url7 = data['URLs'][6];
                url8 = data['URLs'][7];
                url9 = data['URLs'][8];
                url10 = data['URLs'][9];
				url11 = data['URLs'][10];
                url12 = data['URLs'][11];
                url13 = data['URLs'][12];
                url14 = data['URLs'][13];
                url15 = data['URLs'][14];
                url16 = data['URLs'][15];
                url17 = data['URLs'][16];
                url18 = data['URLs'][17];
                url19 = data['URLs'][18];
                url20 = data['URLs'][19];
				$('<img src="' + url1 + '"/>').addClass('a').appendTo('#content');
                $('<img src="' + url2 + '"/>').addClass('b').appendTo('#content');
                $('<img src="' + url3 + '"/>').addClass('c').appendTo('#content');
                $('<img src="' + url4 + '"/>').addClass('d').appendTo('#content');
                $('<img src="' + url5 + '"/>').addClass('e').appendTo('#content');
				$('<img src="' + url6 + '"/>').addClass('f').appendTo('#content');
                $('<img src="' + url7 + '"/>').addClass('g').appendTo('#content');
                $('<img src="' + url8 + '"/>').addClass('h').appendTo('#content');
                $('<img src="' + url9 + '"/>').addClass('i').appendTo('#content');
                $('<img src="' + url10 + '"/>').addClass('j').appendTo('#content');
				$('<img src="' + url11 + '"/>').addClass('k').appendTo('#content');
                $('<img src="' + url12 + '"/>').addClass('l').appendTo('#content');
                $('<img src="' + url13 + '"/>').addClass('m').appendTo('#content');
                $('<img src="' + url14 + '"/>').addClass('n').appendTo('#content');
                $('<img src="' + url15 + '"/>').addClass('o').appendTo('#content');
				$('<img src="' + url16 + '"/>').addClass('p').appendTo('#content');
                $('<img src="' + url17 + '"/>').addClass('q').appendTo('#content');
                $('<img src="' + url18 + '"/>').addClass('r').appendTo('#content');
                $('<img src="' + url19 + '"/>').addClass('s').appendTo('#content');
                $('<img src="' + url20 + '"/>').addClass('t').appendTo('#content');
				window.elements = ['.a','.b','.c','.d','.e','.f','.g','.h','.i','.j','.k','.l','.m','.n','.o','.p','.q','.r','.s','.t'];
            }
			else {
				console.log('Shit didn\'t work!');
			}
			for (i = 0; i < elements.length; i++) {
				animateDiv($(elements[i]));
				focusClick($(elements[i]));
			};
			draggableImage();
			window.delay = setInterval(getImages, delay);
			getSettings();
			$('img').css('border-top-left-radius', slider1_1 + '%');
			$('img').css('border-top-right-radius', slider1_2 + '%');
			$('img').css('border-bottom-left-radius', slider1_3 + '%');
			$('img').css('border-bottom-right-radius', slider1_4 + '%');
			$('img').css('min-width', slider2 + 'px');
			$('img').css('min-height', slider2 + 'px');
			$('img').css('max-width', slider3 + 'px');
			$('img').css('max-height', slider3 + 'px');
			$('img').css('max-height', slider3 + 'px');
			$('img').css('box-shadow', slider4 + 'px ' + slider4 + 'px ' + slider4 + 'px #000');
		});
    return false;
};

// Functions to get the number of GIFs requested from the session
$(document).ready(function() {
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
});

// Functions to select category
$(document).ready(function() {
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
});

// Function to handle auto refresh
$(document).ready(function() {
	$('#submit').click(function() {
		var data = $('#delay').val();
		console.log(data);
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
});


// Function to display the current settings
function getSettings() {
	$('.setting').remove();
	$.getJSON($SCRIPT_ROOT + '/gif_party_json',
		function(data) {
			var category = data['category'];
			var number = data['number'];
			var delay = data['delay'];
			delay = String(delay).slice(0, 2);
			$('<p>' + category + '</p><br>').addClass('setting').appendTo('#settings-values');
			$('<p>' + number + '</p><br>').addClass('setting').appendTo('#settings-values');
			$('<p>' + delay + ' seconds</p><br>').addClass('setting').appendTo('#settings-values');
		});
	};

// Function disable pressing ENTER in the textfield
// Need user to hit 'submit' to trigger JavaScript function
$(document).ready(function() {
	$('#delay').keypress(function(e){
	   if (e.keyCode == 13) return false
	});
});