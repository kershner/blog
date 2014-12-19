function cms() {
	showColorSelect();
	showIconSelect();
	colorSelect();
	iconSelect();
	masonry();
	populateData();
	preview();
	confirmation();
	inputLabels();
	showFormatting();
	instantPreview();
	showHiddenFields();
	centerImages();
	addTags();
}

function populateData(data) {
	console.log('Populating data...!');
	$('.preview').fadeOut('fast');		
	$('.posts-container').fadeOut('fast');
	var color = $('#color').val();
	var title = $('#title').val();
	var icon = $('#icon').val();
	var subtitle = $('#subtitle').val();
	var content = $('#content').val();
	var hidden_date = $('#hidden_date').val();
	
	$.getJSON($SCRIPT_ROOT + '/preview', {
		color: color,
		title: title,
		icon: icon,
		subtitle: subtitle,
		content: content,
		hidden_date: hidden_date
	}, function(data) {
		$('.preview').fadeIn('fast');
		$('.preview').empty();
		$('.preview').append(data.html); 
		// if ($('.preview code').length > 0) {
		// 	var html = '<script>Rainbow.color();</script>'
		// 	$('.preview code').addClass('rainbow');
		// 	$('.preview').append(html);
		// 	console.log('Script element appended');
		// }	 	
	});
	return false;
}

function preview() {
	$('#preview').on('click', function() {
		populateData();
	});
}

function colorSelect() {
	var clicked = false;
	$('#color-selections div').on('click', function() {
		var color = $(this).css('background-color');
		$('#color').val(color);
		$('#color-selections > div').css('box-shadow', '1px 1px 3px #000');
		$(this).css('box-shadow', '0px 0px 10px #1c87ff');
		populateData();
		notSubmitted();
	});
}

function iconSelect() {
	$('#icon-selections img').on('click', function() {
		$('#icon').val($(this).get(0).src);
		$('#icon-selections > *').css('border-bottom', '2px solid Transparent');
		$(this).css('border-bottom', '2px solid #1c87ff');
		populateData();
		notSubmitted();
	});
}

function showColorSelect() {
	var clicked = false;
	$('#color-select').on('click', function() {
		if (clicked) {
			clicked = false;
			$('#color-selections').fadeOut('fast');
			$(this).removeClass('color-select-selected');
		}
		else {
			clicked = true;
			$('#color-selections').fadeIn('fast');
			$(this).addClass('color-select-selected');
		}
	});
}

function showIconSelect() {
	var clicked = false;
	$('#icon-select').on('click', function() {
		if (clicked) {
			clicked = false;
			$('#icon-selections').fadeOut('fast');
			$(this).removeClass('color-select-selected');		
		}
		else {
			clicked = true;
			$('#icon-selections').fadeIn('fast');
			$(this).addClass('color-select-selected');
		}
	});
}

function masonry() {
	var containerDivs = [
		'#current-posts-container',
		'#old-posts-container',
		'#last-month-posts-container',
		'#two-months-ago-posts-container'		
	];
	
	for (i = 0; i < containerDivs.length; i++) {
		$(containerDivs[i]).masonry({
			itemSelector: '.post-thumb',
			'isFitWidth': true,
		});
	}
}

function confirmation() {
	$('#delete').on('click', function() {
		$('.confirm').fadeIn('fast');
		$('#delete').fadeOut('fast');
		$('#confirm-no').on('click', function() {
			$('div.confirm').fadeOut('fast');
			$('#delete').fadeIn('fast');
		});
	});
}

function inputLabels() {
	var title = $('#title').val();
	var subtitle = $('#subtitle').val();
	var content = $('#content').val();
	
	if (title) {
		if (title.length > 1) {
			$('#title-label').css('color', 'black');
		}
		if (subtitle.length > 1) {
			$('#date-label').css('color', 'black');
		}
		if (content.length > 1) {
			$('#content-label').css('color', 'black');
		}
	}
	
	$('#title').on('input', function() {
		var title = $('#title').val();
		if (title.length < 1) {
			$('#title-label').css('color', 'white');
		}
		else {
			$('#title-label').css('color', 'black');
			notSubmitted();
		}
	});
	
	$('#subtitle').on('input', function() {
		var subtitle = $('#subtitle').val();
		if (subtitle.length < 1) {
			$('#date-label').css('color', 'white');
		}
		else {
			$('#date-label').css('color', 'black');
			notSubmitted();
		}
	});
	
	$('#content').on('input', function() {
		var content = $('#content').val();
		if (content.length < 1) {
			$('#content-label').css('color', 'white');
		}
		else {
			$('#content-label').css('color', 'black');
			notSubmitted();
		}
	});
}

function notSubmitted() {
	$('.not-submitted').fadeIn('fast');
}

function showFormatting() {
	var clicked = false;
	$('#formatting').on('click', function() {
		if (clicked) {
			clicked = false;
			$('.format-guide').fadeOut('fast');
			$(this).removeClass('color-select-selected');		
		}
		else {
			clicked = true;
			$('.format-guide').fadeIn('fast');
			$(this).addClass('color-select-selected');
		}
	});
}

function detectInput(element) {
	$(element).one('keypress', function() {
		$(element).focusout(function() {
			populateData();
		});
	});
}

function instantPreview() {
	detectInput('#title');
	detectInput('#subtitle');
	detectInput('#content');
}

function showHiddenFields() {
	var clicked = false;
	$('#show-hidden').on('click', function() {
		if (clicked) {
			clicked = false;
			$('#hidden_date').fadeOut('fast');
			$('#month').fadeOut('fast');
			$('#year').fadeOut('fast');
		}
		else {
			clicked = true;
			$('#hidden_date').fadeIn('fast');
			$('#month').fadeIn('fast');
			$('#year').fadeIn('fast');
		}
	});
}


function centerImages() {
	if ($('.white p img').length > 0) {
		$('.white p img').parent().css({
			'width' : '90%',
			'margin' : '0 auto',
			'text-align' : 'center',
		});
	}
	var iframes = document.getElementsByTagName('iframe');
	if (iframes.length > 0) {
		$(iframes).parent().css({
			'width' : '75%',
			'margin' : '0 auto',
			'text-align' : 'center',
		});
	}
}

// Masonry for /projects route
function projectsMasonry() {
	var masonry = new Masonry('#projects-grid', {
		itemSelector: '.project'
	});
	
	imagesLoaded('#projects-grid', function() {
		masonry.layout();
	});
}

function codeTags() {
	var clicked = false;
	$('#code-tag').on('click', function() {
        if (clicked) {
        	clicked = false;        	
        	$('#code-tag-options').fadeOut('fast');
        	$(this).removeClass('color-select-selected');
        	$('.format-guide').css('height', '-=40px');
    	} else {
    		clicked = true;
    		$('#code-tag-options').fadeIn('fast');    		
        	$(this).addClass('color-select-selected');
        	$('.format-guide').css('height', '+=40px');
    	}
    });
    $('#code-tag-options-python').on('click', function() {
        $('#content').surroundSelectedText('<pre><code data-language="python">', '</code></pre>');
        populateData();
    });
    $('#code-tag-options-js').on('click', function() {
        $('#content').surroundSelectedText('<pre><code data-language="javascript">', '</code></pre>');
        populateData();
    });
}

function headerTags() {
	var clicked = false;
	$('#header-tag').on('click', function() {
        if (clicked) {
        	clicked = false;
        	$('#header-tag-options').fadeOut('fast');
        	$(this).removeClass('color-select-selected');
        	$('.format-guide').css('height', '-=60px');
    	} else {
    		clicked = true;
    		$('#header-tag-options').fadeIn('fast');
        	$(this).addClass('color-select-selected');
        	$('.format-guide').css('height', '+=60px');
    	}
    });
    $('#header-tag-options-h1').on('click', function() {
        $('#content').surroundSelectedText('#', '');
        populateData();
    });
    $('#header-tag-options-h2').on('click', function() {
        $('#content').surroundSelectedText('##', '');
        populateData();
    });
    $('#header-tag-options-h3').on('click', function() {
        $('#content').surroundSelectedText('###', '');
        populateData();
    });
    $('#header-tag-options-h4').on('click', function() {
        $('#content').surroundSelectedText('####', '');
        populateData();
    });
    $('#header-tag-options-h5').on('click', function() {
        $('#content').surroundSelectedText('#####', '');
        populateData();
    });
    $('#header-tag-options-h6').on('click', function() {
        $('#content').surroundSelectedText('#####', '');
        populateData();
    });
}

function boldTag() {
	$('#bold-tag').on('click', function() {
		$('#content').surroundSelectedText('**', '**');
		populateData();
	});
}

function italicTag() {
	$('#italic-tag').on('click', function() {
		$('#content').surroundSelectedText('*', '*');
		populateData();
	});
}

function colorTags() {
	var clicked = false;
	$('#color-tag').on('click', function() {
        if (clicked) {
        	clicked = false;
        	$('#color-tag-options').fadeOut('fast');
        	$(this).removeClass('color-select-selected');
        	$('.format-guide').css('height', '-=40px');
    	} else {
    		clicked = true;
    		$('#color-tag-options').fadeIn('fast');
        	$(this).addClass('color-select-selected');
        	$('.format-guide').css('height', '+=40px');
    	}
    });
    $('#color-tag-options-red').on('click', function() {
    	$('#content').surroundSelectedText('<red>', '</red>');
    	populateData();
    });
    $('#color-tag-options-blue').on('click', function() {
    	$('#content').surroundSelectedText('<blue>', '</blue>');
    	populateData();
    });
    $('#color-tag-options-yellow').on('click', function() {
    	$('#content').surroundSelectedText('<yellow>', '</yellow>');
    	populateData();
    });
    $('#color-tag-options-green').on('click', function() {
    	$('#content').surroundSelectedText('<green>', '</green>');
    	populateData();
    });
    $('#color-tag-options-purple').on('click', function() {
    	$('#content').surroundSelectedText('<purple>', '</purple>');
    	populateData();
    });
}

function linkTag() {
	var clicked = false;
	$('#link-tag').on('click', function() {
		if (clicked) {
			clicked = false;
			$('#link-tag-options').fadeOut('fast');
			$(this).removeClass('color-select-selected');
			$('.format-guide').css('height', '-=115x');
		} else {
			clicked = true;
			$('#link-tag-options').fadeIn('fast');
			$(this).addClass('color-select-selected');
			$('.format-guide').css('height', '+=115px');
		}
	});
	$('#link-tag-submit').on('click', function() {
		var url = $('#link-url').val();		
		$('#content').surroundSelectedText('[', '](' + url + ')')
	});
}

function imgTag() {
	var clicked = false;
	$('#img-tag').on('click', function() {
		if (clicked) {
			clicked = false;
			$('#img-tag-options').fadeOut('fast');
			$(this).removeClass('color-select-selected');
			$('.format-guide').css('height', '-=160x');
		} else {
			clicked = true;
			$('#img-tag-options').fadeIn('fast');
			$(this).addClass('color-select-selected');
			$('.format-guide').css('height', '+=160px');
		}
	});
	$('#img-tag-submit').on('click', function() {
		var url = $('#img-url').val();
		var alt = $('#img-alt-text').val();
		var tag = '![' + alt + '](' + url + ')';
		$('#content').surroundSelectedText(tag, '');
	});
}

function carouselTag() {
	var clicked = false;
	$('#carousel-tag').on('click', function() {
		if (clicked) {
			clicked = false;
			$('#carousel-tag-options').fadeOut('fast');
			$(this).removeClass('color-select-selected');
			$('.format-guide').css('height', '-=110x');
		} else {
			clicked = true;
			$('#carousel-tag-options').fadeIn('fast');
			$(this).addClass('color-select-selected');
			$('.format-guide').css('height', '+=110x');
		}
	});
	$('#add-field').on('click', function() {
		var html = '<input type="text" class="carousel-url" placeholder="URL">';
		$(html).insertBefore($('#add-field'));
	});
	$('#carousel-tag-submit').on('click', function() {
		var inputs = $('#carousel-tag-options').find('input');
		var urls = [];
		var htmlString = '';
		var imageSlickStart = '<div class="slick-images">';		
		var imageSlickEnd = '</div>';
		inputs.each(function() {
			urls.push($(this).val());
		});		
		for (var i = urls.length - 1; i >= 0; i--) {
			tempString = '<div><a href="' + urls[i] + '"><img src="' + urls[i] + '" class="rounded-images"></a></div>';
			htmlString += tempString;
		};
		$('#content').surroundSelectedText(imageSlickStart + htmlString + imageSlickEnd, '');
	});
}

function videoTag() {
	$('#video-tag').on('click', function() {
		$('#content').surroundSelectedText('<div class="video-wrapper">', "</div>");
	});
}

function addTags() {
	codeTags();
	boldTag();
	italicTag();
	headerTags();
	colorTags();
	linkTag();
	imgTag();
	carouselTag();
	videoTag();
}

function initSlick() {
	options = {
		autoplay: true,
		autoplaySpeed: 3000,
		fade: true,
		dots: true,
		pauseOnHover: true,
		nextArrow: '<i></i>',
		prevArrow: '<i></i>'
	}
	$('.slick-images').slick(options);
}
