function screenBloom() {
	callFakeScreenBloom();
}

function callFakeScreenBloom() {
	fakeScreenBloom();
	setInterval(fakeScreenBloom, 3000);
}

function fakeScreenBloom() {
	var color = randomColor();
	var newBoxShadow = '0 0 10vw 1vw ' + color
	var elements = ['#bloom', '#download-section-title', '#about-section-title'];
	for (i = 0; i < elements.length; i++) {
		$(elements[i]).css({'color': color});
	}	
	$('#logo').css({'box-shadow': newBoxShadow});
	$('#download-link').css({'background-color': color});
}