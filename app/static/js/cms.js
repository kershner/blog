function cms() {
	iconSelect();
	masonry();
	populateData();
	preview();
	confirmation();
	inputLabels();
	instantPreview();
	showHiddenFields();
	centerImages();
	addTags();
}

// AJAX request to /preview view function
function populateData(data) {
	console.log('Populating data...!');
	$('.preview').fadeOut('fast');		
	$('.posts-container').fadeOut('fast');
	var color = $('#color').val();
	var title = $('#title').val();
	var author = $('#author').val();
	var icon = $('#icon').val();
	var subtitle = $('#subtitle').val();
	var content = $('#content').val();
	var hidden_date = $('#hidden_date').val();
	
	$.getJSON($SCRIPT_ROOT + '/preview', {
		color: color,
		title: title,
		author: author,
		icon: icon,
		subtitle: subtitle,
		content: content,
		hidden_date: hidden_date
	}, function(data) {
		$('.preview').fadeIn('fast');
		$('.preview').empty();
		$('.preview').append(data.html);
	});
	return false;
}

function preview() {
	$('#preview').on('click', function() {
		populateData();
	});
}

// Adds a visual indicator that icon has been selected
function iconSelect() {
	$('#icon-selections img').on('click', function() {
		$('#icon').val($(this).get(0).src);
		$('#icon-selections > *').css('border-bottom', '2px solid Transparent');
		$(this).css('border-bottom', '2px solid #1c87ff');
		populateData();
		notSubmitted();
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

// Confirmation box when the delete button is pushed
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

// Adds a label above the input when text is entered
function inputLabels() {
	var title = $('#title').val();
	var subtitle = $('#subtitle').val();
	var content = $('#content').val();
	var author = $('#author').val();
	
	if (title) {
		if (title.length > 1) {
			$('#title-label').css('opacity', '1');
		}
		if (subtitle.length > 1) {
			$('#date-label').css('opacity', '1');
		}
		if (content.length > 1) {
			$('#content-label').css('opacity', '1');
		}
		if (author.length > 1) {
			$('#author-label').css('opacity', '1');
		}
	}
	
	$('#title').on('input', function() {
		var title = $('#title').val();
		if (title.length < 1) {
			$('#title-label').css('opacity', '0.0');
		}
		else {
			$('#title-label').css('opacity', '1');
			notSubmitted();
		}
	});
	
	$('#subtitle').on('input', function() {
		var subtitle = $('#subtitle').val();
		if (subtitle.length < 1) {
			$('#date-label').css('opacity', '0.0');
		}
		else {
			$('#date-label').css('opacity', '1');
			notSubmitted();
		}
	});
	
	$('#content').on('input', function() {
		var content = $('#content').val();
		if (content.length < 1) {
			$('#content-label').css('opacity', '0.0');
		}
		else {
			$('#content-label').css('opacity', '1');
			notSubmitted();
		}
	});

	$('#author').on('input', function() {
		var author = $('#author').val();
		if (author.length < 1) {
			$('#author-label').css('opacity', '0.0');
		}
		else {
			$('#author-label').css('opacity', '1');
			notSubmitted();
		}
	});
}

// Fades in an indicator that the post has not yet been submitted
function notSubmitted() {
	$('.not-submitted').fadeIn('fast');
}

// Fires the /preview view function when the element loses focus
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
	detectInput('#author');
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


// Centers dynamically placed images and videos
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

//////////////////////////////////////////////
// Functions for applying markdown tags below
function codeTags() {
	var clicked = false;
	$('#code-tag').on('click', function() {
        if (clicked) {
        	clicked = false;        	
        	$('#code-tag-options').fadeOut(50);
        	$(this).removeClass('color-select-selected');
        	$('.format-guide').css('height', '-=45px');
    	} else {
    		clicked = true;
    		$('#code-tag-options').fadeIn('fast');    		
        	$(this).addClass('color-select-selected');
        	$('.format-guide').css('height', '+=45px');
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
        	$('#header-tag-options').fadeOut(50);
        	$(this).removeClass('color-select-selected');
        	$('.format-guide').css('height', '-=40px');
    	} else {
    		clicked = true;    		
        	$(this).addClass('color-select-selected');
        	$('.format-guide').css('height', '+=40px');
        	$('#header-tag-options').fadeIn('fast');
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
        	$('#color-tag-options').fadeOut(50);
        	$(this).removeClass('color-select-selected');
        	$('.format-guide').css('height', '-=40px');
    	} else {
    		clicked = true;    		
        	$(this).addClass('color-select-selected');
        	$('.format-guide').css('height', '+=40px');
        	$('#color-tag-options').fadeIn('fast');
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
			$('.format-guide').css('height', '-=105px');
		} else {
			clicked = true;
			$('#link-tag-options').fadeIn('fast');
			$(this).addClass('color-select-selected');
			$('.format-guide').css('height', '+=105px');
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
			$('#img-tag-options').fadeOut(50);
			$(this).removeClass('color-select-selected');
			$('.format-guide').css('height', '-=155px');
		} else {
			clicked = true;			
			$(this).addClass('color-select-selected');
			$('.format-guide').css('height', '+=155px');
			$('#img-tag-options').fadeIn('fast');
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
			var inputCount = ($('#carousel-tag-options input').length + 1) * 52.5;
			console.log(inputCount);
			$('#carousel-tag-options').fadeOut('fast');
			$('#carousel-tag-options input').slice(1).remove();
			$(this).removeClass('color-select-selected');
			$('.format-guide').css('height', '-=' + inputCount + 'px');
		} else {
			clicked = true;			
			$(this).addClass('color-select-selected');
			$('.format-guide').css('height', '+=105px');
			$('#carousel-tag-options').fadeIn('fast');
		}
	});
	$('#add-field').on('click', function() {
		$('.format-guide').css('height', '+=55px');
		var html = '<input type="text" class="carousel-url animate" placeholder="URL">';
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

// Initialize 'slick' image carousel
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
