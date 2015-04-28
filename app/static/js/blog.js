function blog() {
	smallMenu();
	getImage();
	setInterval(loadBacon, 8000);
}

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
			var offset = scrollTop - 150
			$('.small-logo-container').fadeIn('fast');
		} else {
			$('.small-logo-container').fadeOut('fast');
		}
	});
}

function loadBacon() {
	var path = 'http://www.kershner.org/static/images/bacon';
	var images = [];
	for (i = 1; i < 7; i++) {
		var imagePath = path + i + '.jpg';
		images.push(imagePath);
	};
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

function jPlayer() {
	var html = '<a href="/static/music/25.mp3"><i class="fa fa-download animate"></i></a>';
	$('#song-download').empty();
	$('#song-download').append(html);

	$('#song-selection').on('click', function() {
		$('#loop-selection').removeClass('selection-highlight')
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
		$('#song-selection').removeClass('selection-highlight')
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
		$("#jquery_jplayer_1").jPlayer("destroy");
		$(this).toggleClass('audio-text-highlight').siblings().removeClass('audio-text-highlight');
		var id = $(this).attr('id');
		var url = '/static/music/';
		var html = '<a href="' + url + id + '.mp3"><i class="fa fa-download animate"></i></a>';
		$('#song-download').empty();
		$('#song-download').append(html);
		$('#jquery_jplayer_1').jPlayer({
			ready: function() {
				$(this).jPlayer('setMedia', {
					title: id + '.mp3',
					mp3: url + id + '.mp3',
					poster: getImage()
				});
			$(this).jPlayer('play', 0);
			},
			swfPath: '/js',
			supplied: 'mp3',
			cssSelector: {
				play: '#play-button',
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
	});

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
	for (i = 1; i < 13; i++) {
		var imagePath = path + i + '.jpg';
		images.push(imagePath);
	};
	var item = images[Math.floor(Math.random() * images.length)];
	return item
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
			image = 'music02.jpg'
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

function sendEmail() {
	$('#send').on('click', function() {
		var subject = $('#subject').val();
		var email = $('#email-content').val();
		var myEmail = 'tyler@kershner.org';
		var link = 'mailto:' + myEmail + '?subject=' + subject + '&body=' + email;
		window.location.href = link;
	});
}