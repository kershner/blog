var pi_config = {};

pi_config.config = {
    'colors' 			: ['#DB3340', '#E8B81A', '#20DA9B', '#28ABE3', '#abe328', '#be28e3', '#6028e3'],
	'previousGifsUrl'	: '',
	'gifInfoUrl'		: '',
	'prevClicked'		: false
};

pi_config.init = function() {
	colorElements();
	portletToggles();
	getMoreGifs();
};

function portletToggles() {
	$('#previous-btn').on('click', function() {
		$(this).toggleClass('btn-selected');
		$('#previous').toggleClass('hidden');
		if (!pi_config.config.prevClicked) {
			getPreviousGifs();
			pi_config.config.prevClicked = true;
		}
	});
}

function getMoreGifs() {
	$('.more-gifs').on('click', function() {
		getPreviousGifs();
	});
}

function colorElements() {
	var counter = Math.floor(Math.random() * pi_config.config.colors.length);
	$('.settings-btn').css('background-color', pi_config.config.colors[counter]);
	$('.nav-btn').each(function() {
		counter += 1;
		if (counter > pi_config.config.colors.length - 1) {
			 counter = 0;
		}
		$(this).css('background-color', pi_config.config.colors[counter]);
	});
	$('.portlet-title').each(function() {
		counter += 1;
		if (counter > pi_config.config.colors.length - 1) {
			 counter = 0;
		}
		$(this).css('background-color', pi_config.config.colors[counter]);
	});
}

function getPreviousGifs() {
	var offset = $('.gif-wrapper').length;
	$.ajax({
        url     : pi_config.config.previousGifsUrl + '/' + offset,
        success : function(result) {
            var gifsHtml = getGifHtml(result['gifs']);
			$('#previous').find('.portlet-body').append(gifsHtml);
			gifInfoWindow();
		},
        error   : function(result) {
            console.log(result);
        }
    });
}

function getGifHtml(gifs) {
	var finalHtml = '';
	for (var i=0; i<gifs.length; i++) {
		var gif = gifs[i],
			url = gif.url,
			lastPlayed = moment(gif.last_played).format('D/M h:mm:ss a');
		finalHtml += '<div class="btn gif-wrapper" data-id="' + gif.id + '"><img src="' + url + '"><span class="last-played">' + lastPlayed + '</span></div>';
	}
	return finalHtml;
}

function gifInfoWindow() {
	var wrapper = $('.gif-wrapper');
	wrapper.unbind('click');
	wrapper.on('click', function() {
		console.log('clicked');
		var gifId = $(this).data('id');
		$.ajax({
			url     : pi_config.config.gifInfoUrl + '/' + gifId,
			success : function(result) {
				var gif = result['gif'],
					overlay = $('.lightbox-overlay');
				overlay.find('img').attr('src', gif.url);
				overlay.removeClass('hidden');
			},
			error   : function(result) {
				console.log(result);
			}
		});
	});
}

$('.close-lightbox').on('click', function() {
	$('.lightbox-overlay').addClass('hidden');
});