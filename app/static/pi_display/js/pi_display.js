var pi_display = {};

pi_display.config = {
    'delay'         : 1,
    'gif'           : [],
    'keepGoing'     : true,
    'colors'        : ['#25B972', '#ff6767', '#FFA533', '#585ec7', '#FF8359']
};

pi_display.init = function() {
    turnOff();
    reloadGif();
    getGif();

    $('.loading').colorWave(pi_display.config.colors);
    window.colorWave = setInterval(function() {
        $('.loading').colorWave(pi_display.config.colors);
    }, 3000);
};

function getGif() {
    if (pi_display.config.keepGoing) {
        console.log('keepGoing ENABLED');
        $.ajax({
            url: $SCRIPT_ROOT + '/pi_display_json',
            success: function (json) {
                var gif = json['gif'],
                    gif = 'http://redditmetrics.com/r/StoppedWorking?uri=/r/StoppedWorking.gif',
                    delay = json['delay'],
                    container = $('.container'),
                    html = '<img class="animate" style="opacity: 0;" src="' + gif + '"/>';

                pi_display.config.gif = gif;
                pi_display.config.delay = delay;

                $(html).appendTo(container).load(function() {
                    container.find('img').error(function() {
                       console.log('ERROR');
                    });
                    container.find('img').first().css('opacity', '0').one("webkitTransitionEnd", function () {
                        $(this).remove();
                        container.find('img').css({'opacity': '1.0'});
                        setTimeout(function () {
                            getGif();
                        }, delay);
                    });
                });

                //container.find('img').css('opacity', '0').one("webkitTransitionEnd",
                //    function () {
                //        container.find('img').remove();
                //        $(html).appendTo(container).load(function () {
                //            $(this).css({'opacity': '1.0'});
                //        });
                //        setTimeout(function () {
                //            getGif();
                //        }, delay);
                //    }
                //);
            },
            error: function(xhr, errmsg, err) {
                console.log('Error!');
                console.log(errmsg);
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        });
    } else {
        console.log('keepGoing DISABLED');
        setTimeout(function() {
            getGif();
        }, 2000);
    }
}

function reloadGif() {
    var colors = pi_display.config.colors,
        randColor = colors[Math.floor(Math.random() * colors.length)];

    $('.reload-area').on('click', function() {
        location.reload();
        $(this).animate({
            'opacity'           : 1,
            'background-color'  : randColor
        }, 500, function() {
            $('.new-gif-text').colorWave(colors);
            setInterval(function() {
                $('.new-gif-text').colorWave(colors);
            }, 6000);
        });
    });
}

function turnOff() {
    $('.turn-off').on('click', function(e) {
        console.log('Clicked');
        $('.content-wrapper').toggleClass('hidden');
        pi_display.config.keepGoing = !$(this).hasClass('turn-off-clicked');
    });
}

// ColorWave
(function( $ ) {
  $.fn.colorWave = function(colors) {
    function _colorWave(colors, element) {
      var finalHtml = '';
      var text = $(element).text();
      var defaultColor = $(element).css('color');
      var wait = text.length * 350;
      // Placing <spans> around each letter with class="colorwave"
      var tempHtml = '';
      for (i=0; i<text.length; i++) {
          tempHtml = '<span class="colorwave">' + text[i] + '</span>';
          finalHtml += tempHtml;
      }
      $(element).empty().append(finalHtml);
      _colorLetters(colors, element, wait, defaultColor);
    }
    // Iterates through given color array, applies color to a colorwave span
    function _colorLetters(colors, element, wait, defaultColor) {
        var counter = (Math.random() * (colors.length + 1)) << 0;
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
      _colorWave(pi_display.config.colors, this);
    });
    return this;
  }
}( jQuery ));