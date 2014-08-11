// Creating a global dictionary to be used in the on-click 'focus'
// function (directly below).  I will refactor this at some point when I understand
// JavaScript better
var options = {};

// Function to click on GIF and 'focus' on it - animation stops,
// CSS height/width and Z index get larger.
// Another click sets them to normal
$(document).ready(function() {
	$("img").toggle(function() {
		$(this).stop();
		var orig_height = "height";
		var orig_width = "width";
		options[orig_height] = $(this).css("height");
		options[orig_width] = $(this).css("width");
		$(this).stop(true, true).animate({ width: "+=50%", height: "+=50%" }, "fast");
		$(this).css("z-index", 20);
		animateDiv($(this));
	}, function() {
		$(this).stop().animate(options, "fast");
		$(this).css("z-index", 1);
		animateDiv($(this));
	});
});

// Function to call random 'focus' function on GIFs
$(document).ready(function() {
	setInterval(focusGif, 10000);
});


// Making images draggable
$(function() {
	$("img").draggable({
		start: function(event, ui) {
			$(this).stop();
		},
		stop: function(event, ui) {
			animateDiv($(this));
		}
	});
});

// Functions to control the border-radius slider
function alterBorderRadius() {
	var slider = $("#slider").slider("value");
	$("img").css("border-radius", slider + "%");
	document.getElementById("border_radius").value=slider;
};

$(function() {
	$("#slider").slider({
	  orientation: "horizontal",
	  range: "min",
	  max: 50,
	  min: 5,
	  value: 5,
	  slide: alterBorderRadius,
	  change: alterBorderRadius
	});
});

// Functions to control the min-size slider
function alterImageSize() {
	var slider = $("#slider2").slider("value");
	$("img").css("min-width", slider + "px");
	$("img").css("min-height", slider + "px");
	document.getElementById("min_size").value=slider;
};

$(function() {
	$("#slider2").slider({
	  orientation: "horizontal",
	  range: "min",
	  step: 100,
	  max: 400,
	  value: 0,
	  slide: alterImageSize,
	  change: alterImageSize
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
	console.log(rand_gif);
	var orig_height = "height";
	var orig_width = "width";
	var options1 = {};
	options1[orig_height] = $(rand_gif).css("height");
	options1[orig_width] = $(rand_gif).css("width");
	$(rand_gif).stop(true, true).animate({ width: "+=50%", height: "+=50%" }, 'slow');
	$(rand_gif).css("z-index", 20);
	setTimeout(function() {
		$(rand_gif).stop(true, true).animate(options1, 'slow');
		$(rand_gif).css("z-index", 1);
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