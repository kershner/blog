function getImage() {
    clearInterval(window.delay);
    $('.container img').one("transitionend",
      function(event) {
        $(this).remove();
    });
    $('.container img').css('opacity', '0');
    $.ajax({
        url: $SCRIPT_ROOT + '/pi_display_json',
        success: function(json) {
            url = json['URL'];
            delay = json['delay'];
            $('<img class="animate" style="opacity: 0;" src="' + url + '"/>').appendTo(".container").load(function() {
                $(this).css({'opacity': '1.0'});
            });
            window.delay = setInterval(getImage, delay);
        },
        error: function(xhr, errmsg, err) {
            console.log('Error!');
            console.log(errmsg);
            console.log(xhr.status + ': ' + xhr.responseText);

        }
    });
    return false;
};