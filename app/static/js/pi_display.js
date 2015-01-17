function getImage() {
    clearInterval(window.delay);
    $('img').fadeOut(1000, function() {
        $(this).remove();
    });
    $.getJSON($SCRIPT_ROOT + '/pi_display_json', function(data) {
        url = data['URL'];
        delay = data['delay'];
        $('<img style="display: none;" src="' + url + '"/>').appendTo(".container").load(function() {
            $('.container img').fadeIn(1000);
            $('.container img').imgCentering();
        });
        window.delay = setInterval(getImage, delay);
    });
    return false
};