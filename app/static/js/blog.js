var COLORS = [
	'#0A7ECC', '#189BF2', '#244459', '#C74932', '#F21A18', '#27E300', '#FFA400',
	'#FF6A00'
];

function blog() {
	smallMenu();
	getImage();
	setInterval(loadBacon, 8000);
	$('.small-logo').colorWave(COLORS);
	$('.big-logo-text').colorWave(COLORS);
	$('.project-page-title').each(function() {
		$(this).colorWave(COLORS);
	});

	setInterval(function() {
        $('.small-logo').colorWave(COLORS);
        $('.big-logo-text').colorWave(COLORS);
        $('.project-page-title').each(function() {
            $(this).colorWave(COLORS);
        });
    }, 10000);

	colorProjects();
}

function colorProjects() {
	var randomNumber = Math.floor(Math.random() * COLORS.length),
		counter = randomNumber,
		delay = 75;
	$('.project').each(function() {
		if (counter >= COLORS.length) {
			counter = 0;
		}

		$(this).css({
			'border-color' 	: COLORS[counter],
			'opacity'		: 1
		});
		$(this).find('.project-text').css('background-color', COLORS[counter]);

		counter += 1;
	});

	$('#projects-container').find('img').each(function() {
		if (counter >= COLORS.length) {
			counter = 0;
		}
		counter += 1;
		$(this).css('border-color', COLORS[counter]);
	});
	var selectedTitle = $('.project-title').random();
	colorWave(COLORS, selectedTitle)
	setInterval(function() {
		var selectedTitle = $('.project-title').random();
		colorWave(COLORS, selectedTitle);
	}, 9000);
}

$.fn.random = function() {
  return this.eq(Math.floor(Math.random() * this.length));
};

function projectsMasonry() {
	var masonry = new Masonry('#projects-grid', {
		itemSelector: '.project'
	});
	imagesLoaded('#projects-grid', function() {
		masonry.layout();
	});
}

function smallMenu() {
	$(document).scroll(function() {
		var scrollTop = $(document).scrollTop();
		if (scrollTop > 150) {
			// Fade in small navbar
			var offset = scrollTop - 150;
			$('.small-logo-container').css({
				'opacity': '1.0',
				'z-index': '20'
			});
		} else {
			$('.small-logo-container').css({
				'opacity': '0.0',
				'z-index': '0'
			});
		}
	});
}

function loadBacon() {
	var path = 'http://www.kershner.org/static/images/bacon';
	var images = [];
	for (i = 1; i < 7; i++) {
		var imagePath = path + i + '.jpg';
		images.push(imagePath);
	}
	var item = images[Math.floor(Math.random() * images.length)];
	var html = '<img style="opacity: 0.0" class="small-logo-icon animate" alt="Tyler Kershner" src="' + item + '">';
	$('#small-logo-link').append(html);
	$('#small-logo-link :first-child').animate({
		'opacity': '0.0'
	}, 1200, function() {
		$('#small-logo-link :first-child').remove();
	});
	$('.small-logo-icon').animate({
		'opacity': '1.0'
	}, 800);
}

function musicTitles() {
    $('.welcome-section-title').animate({'opacity': '1.0'}, 1000);
}

function jPlayer() {
	var html = '<a href="/static/music/25.mp3"><i class="fa fa-download animate"></i></a>';
	window.playing = ';'
	window.songs = [];
    window.loops = [];

    $('.song').each(function() {
        var songNumber = $(this).attr('id');

        window.songs.push(songNumber);
	});

	$('.loop').each(function() {
        var loopNumber = $(this).attr('id');

        window.loops.push(loopNumber);
	});

	$('#song-download').empty();
	$('#song-download').append(html);

	$('#song-selection').on('click', function() {
		$('#loop-selection').removeClass('selection-highlight');
		$('#loop-selection').addClass('selection-unhighlight');
		$(this).removeClass('selection-unhighlight');
		$(this).addClass('selection-highlight');
		$('#songs').css({
			'opacity': '1.0',
			'z-index': '2'});
		$('#loops').css({
			'opacity': '0.0',
			'z-index': '0'
		});
	});

	$('#loop-selection').on('click', function() {
		$('#song-selection').removeClass('selection-highlight');
		$('#song-selection').addClass('selection-unhighlight');
		$(this).removeClass('selection-unhighlight');
		$(this).addClass('selection-highlight');
		$('#loops').css({
			'opacity': '1.0',
			'z-index': '2'});
		$('#songs').css({
			'opacity': '0.0',
			'z-index': '0'});
	});

    // Load audio MP3 from user selection
	$('.audio-text').on('click', function() {
	    var id = $(this).attr('id'),
	        nextId = $(this).next().attr('id');
	        firstId = $(this).parent().children().first().attr('id');

		window.playing = id;
		window.nextId = nextId;

		setJplayerMedia(id);
	});

	function highlightMediaRow(audioId) {
        $('.audio-text').each(function() {
           var id = $(this).attr('id');

           if (id === audioId) {
            $(this).addClass('audio-text-highlight');
           } else {
            $(this).removeClass('audio-text-highlight');
           }
        });
        $(this).toggleClass('audio-text-highlight').siblings().removeClass('audio-text-highlight');
	}

	function setJplayerMedia(audioId) {
	    console.log('Poppin off');
	    var url = '/static/music/',
	        html = '<a href="' + url + audioId + '.mp3"><i class="fa fa-download animate"></i></a>';

	    highlightMediaRow(audioId);

	    $("#jquery_jplayer_1").jPlayer("destroy");

	    $('.audio-text').each(function() {
	        var thisId = $(this).attr('id');

            // Set global nextId from selected .audio-text element
            if (thisId === audioId) {
	           var nextId = $(this).next().attr('id');
	           window.nextId = nextId;
            }
	    });

	    if (window.nextId === undefined) {
		    window.nextId = firstId;
		}

	    $('#jquery_jplayer_1').jPlayer({
			ready   : function() {
    				$(this).jPlayer('setMedia', {
    					title: audioId + '.mp3',
    					mp3: url + audioId + '.mp3',
    					poster: getImage()
    				});
		            $(this).jPlayer('play', 0);
			},
			ended   : function() {
			        setJplayerMedia(window.nextId);
			},
			swfPath: '/js',
			supplied: 'mp3',
			cssSelector: {
				play: '#play-button',
				pause: '#pause-button',
				stop: '#stop-button',
				seekBar: '#seek-bar',
				playBar: '#play-bar',
				mute: '#mute',
				volumeMax: '#max-volume',
				volumeBar: '#volume-bar',
				volumeBarValue: '#volume-bar-value',
				currentTime: '#current-time',
				duration: '#duration',
				title: '#song-title'
			},
			size: {
				height: '90%',
				width: '95%'
			},
			useStateClassSkin: true,
			autoBlur: false,
			smoothPlayBar: true,
			keyEnabled: true,
			remainingDuration: true,
			toggleDuration: true
		});
	}

	// Default State
	$("#jquery_jplayer_1").jPlayer({
		ready: function () {
			$(this).jPlayer('setMedia', {
				title: '25.mp3',
				mp3: '/static/music/25.mp3',
				poster: getImage()
			});
		},
		cssSelectorAncestor: '#jp_container_1',
		swfPath: '/js',
		supplied: 'mp3',
		cssSelector: {
			play: '#play-button',
			pause: '#pause-button',
			stop: '#stop-button',
			seekBar: '#seek-bar',
			playBar: '#play-bar',
			mute: '#mute',
			volumeMax: '#max-volume',
			volumeBar: '#volume-bar',
			volumeBarValue: '#volume-bar-value',
			currentTime: '#current-time',
			duration: '#duration',
			title: '#song-title'
		},
		size: {
			height: '90%',
			width: '95%'
		},
		useStateClassSkin: true,
		autoBlur: false,
		smoothPlayBar: true,
		keyEnabled: true,
		remainingDuration: true,
		toggleDuration: true
	});
}

function getImage() {
	var path = '/static/images/dogs/dogs';
	var images = [];
	for (i = 1; i < 12; i++) {
		var imagePath = path + i + '.png';
		images.push(imagePath);
	}
	var item = images[Math.floor(Math.random() * images.length)];
	return item;
}

function closeLightbox() {
	$('#music-lightbox').on('click', function() {
		$('#music-lightbox').css({
			'opacity': '0.0',
			'z-index': '0'});
	});
}

function musicLightbox() {
	$('.music-clickable').on('click', function() {
		var id = $(this).attr('id');
		var path = '/static/images/music/';
		var image = '';

		if (id === 'collage-1') {
			image = 'music06.jpg';
		} else if (id === 'collage-2') {
			image = 'music04.jpg';
		} else if (id === 'collage-3') {
			image = 'music05.jpg';
		} else if (id === 'collage-4') {
			image = 'music07.jpg';
		} else if (id === 'collage-5') {
			image = 'music01.jpg';
		} else if (id === 'collage-6') {
			image = 'music03.jpg';
		} else if (id === 'collage-7') {
			image = 'music02.jpg';
		}

		var html = '<img src="' + path + image + '"><span>(Click anywhere to close)</span>';
		$('#music-lightbox').empty();
		$('#music-lightbox').append(html);
		$('#music-lightbox').css({
			'opacity': '1.0',
			'z-index': '6'});
		closeLightbox();
	});
}

function musicPlayerColors() {
	setInterval(function() {
		console.log('Changing Color!');
		var color = randomColor();
		$('#jquery_jplayer_1').css('background-color', color);
	}, 1200);
}

function sendEmail() {
	// Opens mailto link after some basic form validation
	$('#send').on('click', function() {
		var subjectLength = $('#subject').val().length;
		var bodyLength = $('#email-content').val().length;
		if (subjectLength == 0) {
			console.log('Subject Field is Empty!');
			$('#welcome-subject-notification').css({
			    'opacity': '1.0',
			    'z-index': 2
			});
			setTimeout(function() {
				$('#welcome-subject-notification').css({
				    'opacity': '0.0',
				    'z-index': 0
				});
			}, 3000);
		}
		if (bodyLength == 0) {
			console.log('Body Field is Empty!');
			$('#welcome-body-notification').css({
			    'opacity': '1.0',
			    'z-index': 2
			});
			setTimeout(function() {
				$('#welcome-body-notification').css({
				    'opacity': '0.0',
				    'z-index': 0
				});
			}, 3000);
		}
		if (subjectLength > 0 && bodyLength > 0) {
			var subject = $('#subject').val();
			var email = $('#email-content').val();
			var myEmail = 'tyler@kershner.org';
			var link = 'mailto:' + myEmail + '?subject=' + subject + '&body=' + email;
			window.location.href = link;
		}
	});
}

function welcomeFadeIn() {
    setTimeout(function() {
        $('#blurb01').animate({'opacity': '1.0'}, 800, function() {
			colorWave(COLORS, '#hello');
        	colorWave(COLORS, '#blurb01');
            $('#blurb02').animate({'opacity': '1.0'}, 900, function() {
                colorWave(COLORS, '#blurb02');
                $('#blurb03').animate({'opacity': '1.0'}, 900, function() {
                	colorWave(COLORS, '#blurb03');
                });
                $('#welcome-pic').animate({'opacity': '1.0'}, 1000);
                $('#down-arrow').animate({'opacity': '1.0'}, 800);
                blinkingArrow();
                welcomeScroll();
            });
        });
        colorWave(COLORS, '#projects-title');
        colorWave(COLORS, '#contact-title');
        $('.welcome-project-inner-title').each(function() {
        	colorWave(COLORS, $(this));
        });
    }, 500);
}

function welcomeScroll() {
    var waypoint = new Waypoint({
        element: $('#welcome-pic'),
        handler: function() {
            $('#projects-title, #contact-title').addClass('levitate-smaller');
            $('#projects-section').animate({'opacity': '1.0'}, 800);
        },
        offset: '35%'
    });
    var contactWaypoint = new Waypoint({
    	element: $('#more-projects'),
    	handler: function() {
    		$('#contact-section').animate({'opacity': '1.0'}, 800);
    	},
    	offset: '75%'
    });
}

function blinkingArrow(action) {
    setInterval(function() {
        $('#down-arrow').animate({'opacity': '0.3'}, 1000);
        $('#down-arrow').animate({'opacity': '1.0'}, 1000);
    }, 1000);
}

(function($) {
  $.fn.colorWave = function(colors) {
    function _colorWave(colors, element) {
      var finalHtml = '';
      var text = $(element).text();
      var defaultColor = $(element).css('color');
      var wait = text.length * 350;
      // Placing <spans> around each letter with class="colorwave"
      var tempHtml = '';
      for (i=0; i<text.length; i++) {
          tempHtml = '<span class="colorwave" style="position: relative;">' + text[i] + '</span>';
          finalHtml += tempHtml;
      }
      $(element).empty().append(finalHtml);
      _colorLetters(colors, element, wait, defaultColor);
    }
    // Iterates through given color array, applies color to a colorwave span
    function _colorLetters(colors, element, wait, defaultColor) {
        var randomnumber = (Math.random() * (colors.length + 1)) << 0;
        var counter = randomnumber;
        var delay = 100;
        var adjustedWait = wait / 5;
        $(element).find('.colorwave').each(function() {
            if (counter >= colors.length) {
                counter = 0;
            }
            $(this).animate({
              'color': colors[counter],
              'bottom': '+=6px'
            }, delay);
            delay += 75;
            counter += 1;
        });
        setTimeout(function() {
            _removeColor(element, defaultColor);
        }, adjustedWait);
    }
    // Iterates through color wave spans, returns each to default color
    function _removeColor(element, defaultColor) {
        var delay = 100;
        $(element).find('.colorwave').each(function() {
            $(this).animate({
              'color': defaultColor,
              'bottom': '-=6px'
            }, delay);
            delay += 75;
        });
    }
    return this.each(function() {
      _colorWave(colors, this);
    });
    return this;
  }
}(jQuery));