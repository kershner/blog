var pi_display = {};

pi_display.config = {
    'delay'         : 1,
    'gifs'          : [],
    'colors'        : ['#25B972', '#ff6767', '#FFA533', '#585ec7', '#FF8359']
};

pi_display.init = function() {
    getGifs();
    playGifs();

    $('.loading').colorWave(pi_display.config.colors);
    window.colorWave = setInterval(function() {
        $('.loading').colorWave(pi_display.config.colors);
    }, 3000);
};

function getGifs() {
    $.ajax({
        url: $SCRIPT_ROOT + '/pi_display_json',
        success: function(json) {
            var urls = json['urls'],
                delay = json['delay'];

            pi_display.config.gifs = urls;
            pi_display.config.delay = delay;
            pi_display.config.delay = 20000;
        },
        error: function(xhr, errmsg, err) {
            console.log('Error!');
            console.log(errmsg);
            console.log(xhr.status + ': ' + xhr.responseText);

        }
    });
}

function playGifs() {
    setTimeout(function() {
        var container = $('.container');
        // Randomize array
        pi_display.config.gifs.sort(function() { return 0.5 - Math.random() });

        console.log(pi_display.config.gifs);
        console.log('# of GIFs remaining: ', pi_display.config.gifs.length);
        container.find('img').css('opacity', '0').one("webkitTransitionEnd",
            function() {
                container.find('img').remove();
                $('<img class="animate" style="opacity: 0;" src="' + pi_display.config.gifs.pop() + '"/>').appendTo('.container').load(function() {
                    $(this).css({'opacity': '1.0'});
                });
            }
        );
        if (pi_display.config.gifs.length === 1) {
            console.log('GET NEW URLS, REGEN CONFIG.URLS');
            getGifs();
        }
        playGifs();
    }, pi_display.config.delay)
}

function getImage() {
    var imgContainer = $('.container img');

    clearInterval(window.delay);

    imgContainer.one("webkitTransitionEnd",
      function(event) {
        $(this).remove();
    });
    imgContainer.css('opacity', '0');
    return false;
}

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