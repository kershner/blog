function getImage() {
    clearInterval(window.delay);
    $("img").remove();
    $.getJSON($SCRIPT_ROOT + '/pi_display_json', function(data) {
        url = data["URL"];
        delay = data["delay"];
        $('<img src="' + url + '"/>').appendTo(".container");
        $(".container img").imgCentering();
        window.delay = setInterval(getImage, delay);
    });
    return false
};