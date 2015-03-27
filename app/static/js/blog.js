function blog() {
	smallMenu();
	getImage();
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

function jPlayer() {
	var html = '<a href="/static/music/25.mp3" download>Download</a>';
	$('#song-download').empty();
	$('#song-download').append(html);

	$('#song-selection').on('click', function() {
		$('#loop-selection').removeClass('highlight');
		$(this).addClass('highlight');
		$('#songs').css({
			'opacity': '1.0',
			'z-index': '2'});
		$('#loops').css({
			'opacity': '0.0',
			'z-index': '0'
		});
	});

	$('#loop-selection').on('click', function() {
		$('#song-selection').removeClass('highlight');
		$(this).addClass('highlight');
		$('#loops').css({
			'opacity': '1.0',
			'z-index': '2'});
		$('#songs').css({
			'opacity': '0.0',
			'z-index': '0'});
	});

	$('.audio-text').on('click', function() {		
		$("#jquery_jplayer_1").jPlayer("destroy");
		$(this).toggleClass('audio-text-highlight').siblings().removeClass('audio-text-highlight');
		var id = $(this).attr('id');
		var url = '/static/music/';
		var html = '<a href="' + url + id + '.mp3" download>Download</a>';
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
			size: {
				height: '50%',
				width: '80%'
			},
			useStateClassSkin: true,
			autoBlur: false,
			smoothPlayBar: true,
			keyEnabled: true,
			remainingDuration: true,
			toggleDuration: true
		});
	});

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
		size: {
			height: '50%',
			width: '80%'
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
		var myEmail = 'tylerkershner@gmail.com';
		var link = 'mailto:' + myEmail + '?subject=' + subject + '&body=' + email;
		window.location.href = link;
	});
}