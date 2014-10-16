// Hidden Menu Script
function hiddenMenu() {
	$(window).scroll(function() {
		if ($(window).scrollTop() > 325) {
			$("#hidden-menu").fadeIn("fast").css("display", "block");
		}
		else if ($(window).scrollTop() < 326) {
			$("#hidden-menu").fadeOut("fast");
		}
	});
}

function showForm() {
	$("#get-started").one("click", function() {
		$("#form").fadeIn("slow", "linear");		
		$(".select-box").customSelect();
		$("#welcome-header").css("margin-top", "25px");
	});
}

function showDonut(data) {
	$("#donut-selector").click(function() {
		$("#data").fadeOut("fast");
		$("#bar").fadeOut("fast");
		$("#line").fadeOut("fast");
		$("#donut").fadeIn("slow");
		options = {animationSteps: 70, animationEasing: "easeOutExpo"};
		var ctx = $("#donut-chart").get(0).getContext("2d");
		var myDoughnutChart = new Chart(ctx).Doughnut(data, options);
	});
}

function showList() {
	$("#list-selector").click(function() {
		$("#donut").fadeOut("fast");
		$("#bar").fadeOut("fast");
		$("#line").fadeOut("fast");
		$("#data").fadeIn("slow");
	});
}

function showBar(data) {
	$("#bar-selector").click(function() {
		$("#donut").fadeOut("fast");
		$("#data").fadeOut("fast");
		$("#line").fadeOut("fast");
		$("#bar").fadeIn("slow");
		options = {scaleFontColor: "#FFFFFF"};
		var ctx = $("#bar-chart").get(0).getContext("2d");
		var myBarChart = new Chart(ctx).Bar(data, options);
	});
}

function showLine(data) {
	$("#line-selector").click(function() {
		$("#donut").fadeOut("fast");
		$("#data").fadeOut("fast");
		$("#bar").fadeOut("fast");
		$("#line").fadeIn("slow");
		options = {scaleFontColor: "#FFFFFF"};
		var ctx = $("#line-chart").get(0).getContext("2d");
		var myLineChart = new Chart(ctx).Line(data, options);
	});
}