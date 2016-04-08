var pi_config = {};

pi_config.config = {
    'colors' 			: ['#DB3340', '#E8B81A', '#20DA9B', '#28ABE3', '#abe328', '#be28e3', '#6028e3'],
	'previousGifsUrl'	: '',
	'gifInfoUrl'		: '',
	'addGifUrl'			: '',
	'updateUrl'			: '',
	'removeUrl'			: '',
	'prevClicked'		: false,
	'offset'			: 0,
	'defaultGif'		: 'https://giant.gfycat.com/DeliriousHatefulEkaltadeta.gif'
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

	$('#gifs-btn').on('click', function() {
		$(this).toggleClass('btn-selected');
		$('#gifs').toggleClass('hidden');

		// Add Gifs Button inside #gifs portlet
		$('#add-gif-btn').on('click', function() {
			gifInfoWindow({}, 'add');
		});
	});
}

function getMoreGifs() {
	$('.more-gifs').on('click', function() {
		getPreviousGifs();
	});
}

function colorElements() {
	var counter = Math.floor(Math.random() * pi_config.config.colors.length);
	$('.settings-btn i').css('color', pi_config.config.colors[counter]);
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
	$.ajax({
        url     : pi_config.config.previousGifsUrl + '/' + pi_config.config.offset,
        success : function(result) {
			appendGifsHtml(result['gifs']);
			clickGifs();
			pi_config.config.offset += 10;
		},
        error   : function(result) {
            console.log(result);
        }
    });
}

function appendGifsHtml(gifs) {
	var container = $('#previous').find('.portlet-body'),
		addedIds = [];
	for (var i=0; i<gifs.length; i++) {
		var gif = gifs[i],
			url = gif.url,
			lastPlayed = moment(gif.last_played).subtract(4, 'hours').format('MMM Do h:mm:ss a');
		addedIds.push(gif.id);
		$('<div class="btn gif-wrapper" data-id="' + gif.id + '"><img src="' + url + '"><span class="last-played">' + lastPlayed + '</span></div>').appendTo(container);
	}
	for (var j=0; j<addedIds.length; j++) {
		$('[data-id="' + addedIds[j] + '"]').addClass('fadeIn');
	}
}

function clickGifs() {
	var wrapper = $('.gif-wrapper');
	wrapper.unbind('click');
	wrapper.on('click', function() {
		var gifId = $(this).data('id');
		$.ajax({
			url     : pi_config.config.gifInfoUrl + '/' + gifId,
			success : function(result) {
				$('#add-gif-form').data('gif-id', result['gif']['id']);
				gifInfoWindow(result['gif'], 'update');
			},
			error   : function(result) {
				console.log(result);
			}
		});
	});
}

function gifInfoWindow(gif, method) {
	var overlay = $('.lightbox-overlay'),
		form = $('#add-gif-form');
	if (method === 'add') {
		overlay.find('img').attr('src', pi_config.config.defaultGif);
		overlay.removeClass('hidden');

		form.data('gif-id', null);
		$('#url-input, #desc-input, #tags-input').val('');

		form.find('.btn').addClass('hidden');
		$('.add-gif, .remove-gif').removeClass('hidden');
	} else if (method === 'update') {
		overlay.find('img').attr('src', gif.url);
		overlay.removeClass('hidden');

		$('.gif-tags-container').empty();
		console.log(gif.tags);
		for (var i=0; i<gif.tags.length; i++) {
			var tagHtml = '<div class="tag"><i class="fa fa-tag"></i>' + gif.tags[i] + '</div>';
			$('.gif-tags-container').append(tagHtml);
		}

		$('#url-input').val(gif.url);
		$('#desc-input').val(gif.description);
		$('.save-gif').text('Update GIF');

		form.find('.btn').addClass('hidden');
		$('.remove-gif, .update-gif').removeClass('hidden');
	} else if (method === 'remove') {
		console.log('Adding GIF to bad urls list...')
	}
}

// General events
$('.remove-gif').on('click', function() {
	$('#add-gif-form').data('ajax-url', pi_config.config.removeUrl);
});

$('.add-gif').on('click', function() {
	$('#add-gif-form').data('ajax-url', pi_config.config.addGifUrl);
});

$('.update-gif').on('click', function() {
	$('#add-gif-form').data('ajax-url', pi_config.config.updateUrl);
});

$('#add-gif-form').on('submit', function() {
	var gif = {
		'url'		: $('#url-input').val(),
		'tags'		: $('#tags-input').val(),
		'desc'		: $('#desc-input').val(),
		'id'		: $(this).data('gif-id')
	};

	$.ajax({
		url     	: $(this).data('ajax-url'),
		method		: 'POST',
		contentType	: 'application/json;charset=UTF-8',
		data		: JSON.stringify(gif),
		success : function(result) {
			console.log(result);
			console.log('NO ERROR');
			// Pop up notification
		},
		error   : function(result) {
			console.log(result);
			if (result.status === 401) {
				console.log('ACCESS DENIED');
				window.location = '/login'
			}
			// Pop up notification
		}
	});
	return false;
});

$('.close-lightbox').on('click', function() {
	$('.lightbox-overlay').addClass('hidden');
});

$('#url-input').on('input', function() {
	var overlay = $('.lightbox-overlay');
	if (endsWith($(this).val(), '.gif')) {
		overlay.find('img').attr('src', $(this).val());
	} else {
		overlay.find('img').attr('src', pi_config.config.defaultGif);
	}
});

// Utility
function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}