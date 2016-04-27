var pi_config = {};

pi_config.config = {
    'colors' 			: ['#DB3340', '#E8B81A', '#20DA9B', '#28ABE3', '#abe328', '#be28e3', '#6028e3'],
	'previousGifsUrl'	: '',
	'gifInfoUrl'		: '',
	'addGifUrl'			: '',
	'updateUrl'			: '',
	'removeUrl'			: '',
	'settingsUrl'		: '',
	'gifsRotationUrl'	: '',
	'offset'			: 0,
	'defaultGif'		: 'https://giant.gfycat.com/DeliriousHatefulEkaltadeta.gif'
};

pi_config.init = function() {
	colorElements();
	mainButtons();
	getMoreGifs();
};

function mainButtons() {
	$('.settings-btn').on('click', function() {
		getGifsInRotation();
		$('.lightbox-overlay').removeClass('hidden');
		$('.settings').removeClass('hidden');
		$('.gif-info-window').addClass('hidden');
	});

	$('#gifs-btn').on('click', function() {
		var container = $('#gifs');
		$(this).toggleClass('btn-selected');
		container.toggleClass('hidden');

		$('#add-gif-btn').on('click', function() {
			gifInfoWindow({}, 'add');
		});

		refreshCurrentGif();
		// Reset gifs container
		if (container.hasClass('hidden')) {
			$('.gif-wrapper').remove();
			pi_config.config.offset = 0;
		} else {
			getPreviousGifs()
		}
	});

	backToTop();
}

function refreshCurrentGif() {
	$.ajax({
			url: pi_config.config.previousGifsUrl + '/0',
			success: function (result) {
				var gifs = result.gifs,
					currentUrl = gifs[0].url;

				$('.current-gif-container').find('img').attr('src', currentUrl);
			},
			error: function (result) {
				console.log(result);
			}
		});
}

function getGifsInRotation() {
	if (!$('#in-rotation').text().length) {
		$.ajax({
			url: pi_config.config.gifsInRotationUrl,
			method: 'POST',
			success: function (result) {
				$('#in-rotation').empty().append(result.total);
			},
			error: function (result) {
				console.log(result);
			}
		});
	}
}

function getMoreGifs() {
	$('.prev-gifs').on('click', function() {
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
	$('#gifs').find('.loading-icon').removeClass('hidden');
	$('.prev-50-text').addClass('hidden');
	$.ajax({
        url     : pi_config.config.previousGifsUrl + '/' + pi_config.config.offset,
        success : function(result) {
			$('#gifs').find('.loading-icon').addClass('hidden');
			$('.prev-50-text').removeClass('hidden');
			appendGifsHtml(result['gifs']);
			clickGifs();
			pi_config.config.offset += 50;
		},
        error   : function(result) {
            console.log(result);
        }
    });
}

function appendGifsHtml(gifs) {
	var container = $('#gifs').find('.portlet-body'),
		addedIds = [];
	for (var i=0; i<gifs.length; i++) {
		var gif = gifs[i],
			url = '/static/pi_display/thumbnails/' + gif.id + '.jpeg',
			lastPlayed = moment(gif.last_played).subtract(4, 'hours').format('MMM Do h:mm:ss a'),
			tags = gif.tags,
			desc = gif.desc ? gif.desc : '',
			html = '<div class="btn gif-wrapper" data-id="' + gif.id + '">' +
				   '<img src="' + url + '"><span class="last-played">' + lastPlayed + '</span>';
		if (tags.length) {
			html += '<i class="fa fa-tag gif-icon gif-tags-icon"></i>';
		}
		if (desc.length) {
			html += '<i class="fa fa-pencil gif-icon gif-desc-icon"></i>';
		}
		html += '</div>';

		addedIds.push(gif.id);
		$(html).appendTo(container);
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

//== General Events ===============================================================================
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
			notification(result['message']);
			infoWindowTeardown(result['type'], result['gif_id']);
		},
		error   : function(result) {
			if (result.status === 401) {
				window.location = '/login'
			}
			notification(result['message']);
		}
	});
	return false;
});

$('#settings-form').on('submit', function() {
	var settings = {
		'delay'			: $('#delay-input').val(),
		'activeTags' 	: $('#active_tag_ids_input').val(),
		'inactiveTags'	: $('#inactive_tag_ids_input').val()
	};

	$.ajax({
		url     	: pi_config.config.settingsUrl,
		method		: 'POST',
		contentType	: 'application/json;charset=UTF-8',
		data		: JSON.stringify(settings),
		success : function(result) {
			console.log(result);
			notification(result['message']);
			$('#in-rotation').text(result['inRotation']);
		},
		error   : function(result) {
			notification(result['message']);
		}
	});
	return false;
});

$('.settings-tag').on('click', function() {
	//$(this).toggleClass('active');
	if ($(this).hasClass('active')) {
		$(this).removeClass('active').addClass('inactive');
	} else if ($(this).hasClass('inactive')) {
		$(this).removeClass('inactive');
	} else {
		$(this).addClass('active');
	}
	updateTagsInput();
});

function updateTagsInput() {
	var activeInputArray = [],
		inactiveInputArray = [];
	$('.settings-tag').each(function() {
		if ($(this).hasClass('active')) {
			activeInputArray.push($(this).data('id'));
		}
		if ($(this).hasClass('inactive')) {
			inactiveInputArray.push($(this).data('id'));
		}
	});
	$('#active_tag_ids_input').val(activeInputArray.toString());
	$('#inactive_tag_ids_input').val(inactiveInputArray.toString());
}
// Lightbox dismissal ////////////////////////////
$('.close-lightbox, .close-settings').on('click', function() {
	infoWindowTeardown('clicked close');
});

$('.lightbox-overlay').on('click', function(e) {
	var target = e.target;
	if ($(target).hasClass('lightbox-overlay')) {
		infoWindowTeardown('clicked out');
	}
});
// End Lightbox dismissal

$('#url-input').on('input', function() {
	var overlay = $('.lightbox-overlay');
	if (endsWith($(this).val(), '.gif')) {
		overlay.find('img').attr('src', $(this).val());
	} else {
		overlay.find('img').attr('src', pi_config.config.defaultGif);
	}
});

//== Utility ======================================================================================
function backToTop() {
	$('.back-to-top').on('click', function() {
		$('html, body').animate({ scrollTop: 0 }, 'slow');
	});
}

function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

function notification(message) {
	var wrapper = $('.notification');
	wrapper.find('p').text(message);
	wrapper.css('opacity', '0.8');
	wrapper.removeClass('hidden');
	setTimeout(function() {
		wrapper.animate({'opacity': 0}, 1000, function() {
			$(this).addClass('hidden');
		});
	}, 2000)
}

// Updates modal DOM elements based on method
function gifInfoWindow(gif, method) {
	$('.settings').addClass('hidden');
	var overlay = $('.lightbox-overlay'),
		infoWindow = $('.gif-info-window'),
		form = $('#add-gif-form');
	if (method === 'add') {
		overlay.find('img').attr('src', pi_config.config.defaultGif);
		overlay.removeClass('hidden');

		form.data('gif-id', null);
		$('#url-input, #desc-input, #tags-input').val('');

		form.find('.btn').addClass('hidden');
		$('.add-gif, .remove-gif').removeClass('hidden');
	} else if (method === 'update') {
		var tagsContainer = $('.gif-tags-container');
		overlay.find('img').attr('src', gif.url);
		overlay.removeClass('hidden');

		tagsContainer.empty();
		for (var i=0; i<gif.tags.length; i++) {
			var tagHtml = '<div class="tag" data-id="' + gif.tags[i].id + '"><i class="fa fa-tag"></i> ' + gif.tags[i] + '</div>';
			tagsContainer.append(tagHtml);
		}

		$('#url-input').val(gif.url);
		$('#tags-input').val('');
		$('#desc-input').val(gif.desc);

		form.find('.btn').addClass('hidden');
		$('.remove-gif, .update-gif').removeClass('hidden');
	}
	infoWindow.removeClass('hidden');
}

function infoWindowTeardown(type, gifId) {
	var wrapper = $('.lightbox-overlay');
	$('.gif-tags-container').empty();
	if (type === 'remove') {
		wrapper.addClass('hidden');
		$('.gif-wrapper').each(function() {
			if ($(this).data('id') === gifId) {
				$(this).remove();
			}
		});
	} else {
		wrapper.addClass('hidden');
	}
}