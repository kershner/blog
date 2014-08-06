$(document).ready(function() {
	$('img').toggle(function() {
		$(this).stop(true, true).animate({ width: "+=10%", height: "+=10%" }, 'fast');
		$(this).css("z-index", 2);
	}, function() {
		$(this).animate({ width: "-=10%", height: "-=10%" }, 'fast');
		$(this).css("z-index", 1);
	});
});

function makeNewPosition($container) {

    // Get viewport dimensions (remove the dimension of the div)
    var h = $container.height() - 200;
    var w = $container.width() - 200;

    var nh = Math.floor(Math.random() * h);
    var nw = Math.floor(Math.random() * w);

    return [nh, nw];

}

function animateDiv($target) {
    var newq = makeNewPosition($target.parent());
    var oldq = $target.offset();
    var speed = calcSpeed([oldq.top, oldq.left], newq);

    $target.animate({
        top: newq[0],
        left: newq[1]
    }, speed, function () {
        animateDiv($target);
    });

};

function calcSpeed(prev, next) {

    var x = Math.abs(prev[1] - next[1]);
    var y = Math.abs(prev[0] - next[0]);

    var greatest = x > y ? x : y;

    var speedModifier = 0.1;

    var speed = Math.ceil(greatest / speedModifier);

    return speed;

}