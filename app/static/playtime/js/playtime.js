function playtime() {
	messageExists();
    showForm();
    showAbout();
    showFindID();
    closeFindID();
    closeAbout();
}

function playtimeResults(data_array) {
	resultsFadeIn();
	showSearch();
	asterisk();
	hallOfShame();
	hiddenMenu();
	smoothTop();
	initialSelections(data_array);
	rangeSelection(data_array);
}

function messageExists() {
	if ($(".message").length > 0) {
		$("#welcome-header, #big-logo, #slogan, #buttons, #footer, #form").fadeIn("fast");		
		$("#welcome-header").css("margin-top", "25px");
		$("#about-content").css("top", "25px");
	} else {
		initialFadeIn();
	};
}

function initialFadeIn() {
	$("#footer").css("display", "none");
	setTimeout(function() {
		$("#welcome-header").fadeIn("fast");
	}, 100);
	setTimeout(function() {
		$("#big-logo").fadeIn("fast");
	}, 500);
	setTimeout(function() {
		$("#slogan").fadeIn("fast");
	}, 1000);
	setTimeout(function() {
		$("#buttons").fadeIn("fast");
		$("#footer").fadeIn("fast");
	}, 1600);
}

function hiddenMenu() {
	$(window).scroll(function() {
		if ($(window).scrollTop() > 315) {
			$("#hidden-menu").fadeIn("fast").css("display", "block");
		}
		else if ($(window).scrollTop() < 316) {
			$("#hidden-menu").fadeOut("fast");
		}
	});
}

function smoothTop() {
	$("#top").click(function() {
		$("html, body").animate({ scrollTop: 0 }, "slow");
	});
}

function showForm() {
	if ($(".message").length > 0) {
		console.log("Blah");
	} else {
		$("#get-started").one("click", function() {
			$("#welcome-header").stop().animate({height : "590px"});
			$("#form").fadeIn("slow", "linear");		
			$("#welcome-header").css("margin-top", "100px");
			$("#welcome-header").css("padding-bottom", "50px");
			$("#about-content").css("top", "25px");
		});
	}
}

function showAbout() {
	$("#about").click(function() {
		$("#about-content").fadeIn("fast");
	});
}

function closeAbout() {
	$("#close").click(function() {
		$("#about-content").fadeOut("fast");
	});
}

function showFindID() {
	$("#where").click(function() {
		$("#find-id").fadeIn("fast");
	});
}

function closeFindID() {
	$("#find-close").click(function() {
		$("#find-id").fadeOut("fast");
	});
}

function resultsFadeIn() {
	setTimeout(function() {
		$("#header").fadeIn("fast");
	}, 200);
	setTimeout(function() {
		$("#user-info").fadeIn("fast");
		$(".result-template").fadeIn("fast");
		$("#search-select").fadeIn("fast");
	}, 400);
}

function showSearch() {
	$("#search-select").click(function() {
		$("#search-select").fadeOut("100");
		$("#new-search").fadeIn("1500");
	});
}

function initialSelections(data_array) {
	$("#list-selector").click(function() {
		showList_2weeks();
	});
	$("#line-selector").click(function() {
		showLine_2weeks(data_array[3]);
	});
	$("#donut-selector").click(function() {
		showDonut_2weeks(data_array[0]);
	});
	$("#bar-selector").click(function() {
		showBar_2weeks(data_array[6]);
	});
}

function hallOfShame() {
	$("#hall-of-shame").click(function() {
		$("#donut_2weeks").fadeOut("fast");
		$("#donut_10").fadeOut("fast");
		$("#donut_20").fadeOut("fast");
		$("#bar_2weeks").fadeOut("fast");
		$("#bar_10").fadeOut("fast");
		$("#bar_20").fadeOut("fast");
		$("#line_2weeks").fadeOut("fast");
		$("#line_10").fadeOut("fast");
		$("#line_20").fadeOut("fast");
		$("#data_2weeks").fadeOut("fast");
		$("#data_10").fadeOut("fast");
		$("#data_20").fadeOut("fast");
		$("#readout_10").fadeOut("fast");
		$("#readout_20").fadeOut("fast");
		$("#readout_2weeks").fadeOut("fast");
		$("#data_all").fadeOut("fast");
		$("#readout_all").fadeIn("slow");
		$("#hall-of-shame-content").fadeIn("slow");
	});
}

function asterisk() {
	$(".asterisk").click(function() {
		$("#asterisk-explanation").fadeIn("fast");
	});
	$("#asterisk-close").click(function() {
		$("#asterisk-explanation").fadeOut("fast");
	});
}

function rangeSelection(data_array) {
	$(".select_donut_2weeks").click(function (){
		showDonut_2weeks(data_array[0]);
	});
	$(".select_donut_10").click(function (){
		showDonut_10(data_array[1]);
	});
	$(".select_donut_20").click(function (){
		showDonut_20(data_array[2]);
	});
	$(".select_line_2weeks").click(function (){
		showLine_2weeks(data_array[3]);
	});
	$(".select_line_10").click(function (){
		showLine_10(data_array[4]);
	});
	$(".select_line_20").click(function (){
		showLine_20(data_array[5]);
	});
	$(".select_bar_2weeks").click(function (){
		showBar_2weeks(data_array[6]);
	});
	$(".select_bar_10").click(function (){
		showBar_10(data_array[7]);
	});
	$(".select_bar_20").click(function (){
		showBar_20(data_array[8]);
	});	
	$(".select_data_2weeks").click(function (){
		showList_2weeks();
	});
	$(".select_data_10").click(function (){
		showList_10();
	});
	$(".select_data_20").click(function (){
		showList_20();
	});
	$(".select_data_all").click(function (){
		showList_all();
	});	
}

function showDonut_2weeks(data) {
	$("#donut_10").fadeOut("fast");
	$("#donut_20").fadeOut("fast");
	$("#bar_2weeks").fadeOut("fast");
	$("#bar_10").fadeOut("fast");
	$("#bar_20").fadeOut("fast");
	$("#line_2weeks").fadeOut("fast");
	$("#line_10").fadeOut("fast");
	$("#line_20").fadeOut("fast");
	$("#data_2weeks").fadeOut("fast");
	$("#data_10").fadeOut("fast");
	$("#data_20").fadeOut("fast");
	$("#data_all").fadeOut("fast");
	$("#readout_10").fadeOut("fast");
	$("#readout_20").fadeOut("fast");
	$("#readout_all").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_2weeks").fadeIn("slow");
	$("#donut_2weeks").fadeIn("slow");
	options = {animationSteps: 70, animationEasing: "easeOutExpo"};
	var ctx = $("#donut-chart_2weeks").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Doughnut(data, options);
}

function showDonut_10(data) {
	$("#donut_2weeks").fadeOut("fast");
	$("#donut_20").fadeOut("fast");
	$("#bar_2weeks").fadeOut("fast");
	$("#bar_10").fadeOut("fast");
	$("#bar_20").fadeOut("fast");
	$("#line_2weeks").fadeOut("fast");
	$("#line_10").fadeOut("fast");
	$("#line_20").fadeOut("fast");
	$("#data_2weeks").fadeOut("fast");
	$("#data_10").fadeOut("fast");
	$("#data_20").fadeOut("fast");
	$("#data_all").fadeOut("fast");
	$("#readout_2weeks").fadeOut("fast");
	$("#readout_20").fadeOut("fast");
	$("#readout_all").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_10").fadeIn("slow");
	$("#donut_10").fadeIn("slow");
	options = {animationSteps: 70, animationEasing: "easeOutExpo"};
	var ctx = $("#donut-chart_10").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Doughnut(data, options);
}

function showDonut_20(data) {
	$("#donut_10").fadeOut("fast");
	$("#donut_2weeks").fadeOut("fast");
	$("#bar_2weeks").fadeOut("fast");
	$("#bar_10").fadeOut("fast");
	$("#bar_20").fadeOut("fast");
	$("#line_2weeks").fadeOut("fast");
	$("#line_10").fadeOut("fast");
	$("#line_20").fadeOut("fast");
	$("#data_2weeks").fadeOut("fast");
	$("#data_10").fadeOut("fast");
	$("#data_20").fadeOut("fast");
	$("#data_all").fadeOut("fast");
	$("#readout_10").fadeOut("fast");
	$("#readout_2weeks").fadeOut("fast");
	$("#readout_all").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_20").fadeIn("slow");
	$("#donut_20").fadeIn("slow");
	options = {animationSteps: 70, animationEasing: "easeOutExpo"};
	var ctx = $("#donut-chart_20").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Doughnut(data, options);
}

function showLine_2weeks(data) {
	$("#donut_2weeks").fadeOut("fast");
	$("#donut_10").fadeOut("fast");
	$("#donut_20").fadeOut("fast");
	$("#bar_2weeks").fadeOut("fast");
	$("#bar_10").fadeOut("fast");
	$("#bar_20").fadeOut("fast");
	$("#line_10").fadeOut("fast");
	$("#line_20").fadeOut("fast");
	$("#data_2weeks").fadeOut("fast");
	$("#data_10").fadeOut("fast");
	$("#data_20").fadeOut("fast");
	$("#data_all").fadeOut("fast");
	$("#readout_10").fadeOut("fast");
	$("#readout_20").fadeOut("fast");
	$("#readout_all").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_2weeks").fadeIn("slow");
	$("#line_2weeks").fadeIn("slow");
	options = {scaleFontColor: "#FFFFFF"};
	var ctx = $("#line-chart_2weeks").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Line(data, options);
}

function showLine_10(data) {
	$("#donut_2weeks").fadeOut("fast");
	$("#donut_10").fadeOut("fast");
	$("#donut_20").fadeOut("fast");
	$("#bar_2weeks").fadeOut("fast");
	$("#bar_10").fadeOut("fast");
	$("#bar_20").fadeOut("fast");
	$("#line_2weeks").fadeOut("fast");
	$("#line_20").fadeOut("fast");
	$("#data_2weeks").fadeOut("fast");
	$("#data_10").fadeOut("fast");
	$("#data_20").fadeOut("fast");
	$("#data_all").fadeOut("fast");
	$("#readout_2weeks").fadeOut("fast");
	$("#readout_20").fadeOut("fast");
	$("#readout_all").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_10").fadeIn("slow");
	$("#line_10").fadeIn("slow");
	options = {scaleFontColor: "#FFFFFF"};
	var ctx = $("#line-chart_10").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Line(data, options);
}

function showLine_20(data) {
	$("#donut_2weeks").fadeOut("fast");
	$("#donut_10").fadeOut("fast");
	$("#donut_20").fadeOut("fast");
	$("#bar_2weeks").fadeOut("fast");
	$("#bar_10").fadeOut("fast");
	$("#bar_20").fadeOut("fast");
	$("#line_2weeks").fadeOut("fast");
	$("#line_10").fadeOut("fast");
	$("#data_2weeks").fadeOut("fast");
	$("#data_10").fadeOut("fast");
	$("#data_20").fadeOut("fast");
	$("#data_all").fadeOut("fast");
	$("#readout_10").fadeOut("fast");
	$("#readout_2weeks").fadeOut("fast");
	$("#readout_all").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_20").fadeIn("slow");
	$("#line_20").fadeIn("slow");
	options = {scaleFontColor: "#FFFFFF"};
	var ctx = $("#line-chart_20").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Line(data, options);
}

function showBar_2weeks(data) {
	$("#donut_2weeks").fadeOut("fast");
	$("#donut_10").fadeOut("fast");
	$("#donut_20").fadeOut("fast");
	$("#bar_10").fadeOut("fast");
	$("#bar_20").fadeOut("fast");
	$("#line_2weeks").fadeOut("fast");
	$("#line_10").fadeOut("fast");
	$("#line_20").fadeOut("fast");
	$("#data_2weeks").fadeOut("fast");
	$("#data_10").fadeOut("fast");
	$("#data_20").fadeOut("fast");
	$("#data_all").fadeOut("fast");
	$("#readout_10").fadeOut("fast");
	$("#readout_20").fadeOut("fast");
	$("#readout_all").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_2weeks").fadeIn("slow");
	$("#bar_2weeks").fadeIn("slow");
	options = {scaleFontColor: "#FFFFFF"};
	var ctx = $("#bar-chart_2weeks").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Bar(data, options);
}

function showBar_10(data) {
	$("#donut_2weeks").fadeOut("fast");
	$("#donut_10").fadeOut("fast");
	$("#donut_20").fadeOut("fast");
	$("#bar_2weeks").fadeOut("fast");
	$("#bar_20").fadeOut("fast");
	$("#line_2weeks").fadeOut("fast");
	$("#line_10").fadeOut("fast");
	$("#line_20").fadeOut("fast");
	$("#data_2weeks").fadeOut("fast");
	$("#data_10").fadeOut("fast");
	$("#data_20").fadeOut("fast");
	$("#data_all").fadeOut("fast");
	$("#readout_2weeks").fadeOut("fast");
	$("#readout_20").fadeOut("fast");
	$("#readout_all").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_10").fadeIn("slow");
	$("#bar_10").fadeIn("slow");
	options = {scaleFontColor: "#FFFFFF"};
	var ctx = $("#bar-chart_10").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Bar(data, options);
}

function showBar_20(data) {
	$("#donut_2weeks").fadeOut("fast");
	$("#donut_10").fadeOut("fast");
	$("#donut_20").fadeOut("fast");
	$("#bar_2weeks").fadeOut("fast");
	$("#bar_10").fadeOut("fast");
	$("#line_2weeks").fadeOut("fast");
	$("#line_10").fadeOut("fast");
	$("#line_20").fadeOut("fast");
	$("#data_2weeks").fadeOut("fast");
	$("#data_10").fadeOut("fast");
	$("#data_20").fadeOut("fast");
	$("#data_all").fadeOut("fast");
	$("#readout_10").fadeOut("fast");
	$("#readout_2weeks").fadeOut("fast");
	$("#readout_all").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_20").fadeIn("slow");
	$("#bar_20").fadeIn("slow");
	options = {scaleFontColor: "#FFFFFF"};
	var ctx = $("#bar-chart_20").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Bar(data, options);
}

function showList_2weeks() {
	$("#donut_2weeks").fadeOut("fast");
	$("#donut_10").fadeOut("fast");
	$("#donut_20").fadeOut("fast");
	$("#bar_2weeks").fadeOut("fast");
	$("#bar_10").fadeOut("fast");
	$("#bar_20").fadeOut("fast");
	$("#line_2weeks").fadeOut("fast");
	$("#line_10").fadeOut("fast");
	$("#line_20").fadeOut("fast");
	$("#data_10").fadeOut("fast");
	$("#data_20").fadeOut("fast");
	$("#data_all").fadeOut("fast");
	$("#readout_10").fadeOut("fast");
	$("#readout_20").fadeOut("fast");
	$("#readout_all").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_2weeks").fadeIn("slow");
	$("#data_2weeks").fadeIn("slow");
}

function showList_10() {
	$("#donut_2weeks").fadeOut("fast");
	$("#donut_10").fadeOut("fast");
	$("#donut_20").fadeOut("fast");
	$("#bar_2weeks").fadeOut("fast");
	$("#bar_10").fadeOut("fast");
	$("#bar_20").fadeOut("fast");
	$("#line_2weeks").fadeOut("fast");
	$("#line_10").fadeOut("fast");
	$("#line_20").fadeOut("fast");
	$("#data_2weeks").fadeOut("fast");
	$("#data_20").fadeOut("fast");
	$("#data_all").fadeOut("fast");
	$("#readout_2weeks").fadeOut("fast");
	$("#readout_20").fadeOut("fast");
	$("#readout_all").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_10").fadeIn("slow");
	$("#data_10").fadeIn("slow");
}

function showList_20() {
	$("#donut_2weeks").fadeOut("fast");
	$("#donut_10").fadeOut("fast");
	$("#donut_20").fadeOut("fast");
	$("#bar_2weeks").fadeOut("fast");
	$("#bar_10").fadeOut("fast");
	$("#bar_20").fadeOut("fast");
	$("#line_2weeks").fadeOut("fast");
	$("#line_10").fadeOut("fast");
	$("#line_20").fadeOut("fast");
	$("#data_2weeks").fadeOut("fast");
	$("#data_10").fadeOut("fast");
	$("#data_all").fadeOut("fast");
	$("#readout_2weeks").fadeOut("fast");
	$("#readout_10").fadeOut("fast");
	$("#readout_all").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_20").fadeIn("slow");
	$("#data_20").fadeIn("slow");
}

function showList_all() {
	$("#donut_2weeks").fadeOut("fast");
	$("#donut_10").fadeOut("fast");
	$("#donut_20").fadeOut("fast");
	$("#bar_2weeks").fadeOut("fast");
	$("#bar_10").fadeOut("fast");
	$("#bar_20").fadeOut("fast");
	$("#line_2weeks").fadeOut("fast");
	$("#line_10").fadeOut("fast");
	$("#line_20").fadeOut("fast");
	$("#data_2weeks").fadeOut("fast");
	$("#data_10").fadeOut("fast");
	$("#data_20").fadeOut("fast");
	$("#readout_10").fadeOut("fast");
	$("#readout_20").fadeOut("fast");
	$("#readout_2weeks").fadeOut("fast");
	$("#hall-of-shame-content").fadeOut("fast");
	$("#readout_all").fadeIn("slow");
	$("#data_all").fadeIn("slow");
}