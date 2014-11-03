function playtime() {
	messageExists();
    showForm();
    showAbout();
    showFindID();
    closeFindID();
    closeAbout();
	dimmer();
}

function playtimeResults(data_array, privacy) {
	resultsFadeIn();
	showSearch();
	asterisk();
	hallOfShame();
	hiddenMenu();
	smoothTop();
	showLegend();
	getFriendId();
	showFriends();
	tabExpand();
	if (privacy === undefined) {
		initialSelections(data_array);
	}
	else { 
		initialSelectionsPrivacy(data_array);
	}
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

function dimmer() {
	$(".submit").click(function() {
		$("#loading-dimmer").css("top", "0").fadeIn("slow");
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
		$("#search-select").animate({"margin-bottom" : "15px"}, 100, function () {
			$("#new-search").fadeIn("slow");
		});		
	});
}

function initialSelectionsPrivacy(data_array) {
	$("#list-selector").click(function() {
		showList_10();
	});
	$("#line-selector").click(function() {
		showLine_10(data_array[4]);
	});
	$("#donut-selector").click(function() {
		showDonut_10(data_array[1]);
	});
	$("#bar-selector").click(function() {
		showBar_10(data_array[7]);
	});
	setTimeout(function() {
		$("#privacy-dimmer").fadeIn("fast");
	}, 200);
	setTimeout(function() {
		$(".result-template").fadeIn("fast");
		$("#data_10").fadeIn("fast");
	}, 400);
	closePrivacyNotice();
}

function closePrivacyNotice() {
	$("#close-privacy").click(function() {
		$("#privacy-dimmer").fadeOut("fast");
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

function showLegend() {
	$(".legend-toggle").click(function() {
		$(".legend, #split").fadeToggle("slow");		
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

function displayElements(fade1, fade2) {
    var elements = [
	"#donut_2weeks", "#donut_10", "#donut_20", "#bar_2weeks",
	"#bar_10", "#bar_20", "#line_2weeks", "#line_10", "#line_20",
	"#data_2weeks", "#data_10", "#data_20", "#readout_10", "#readout_20",
	"#readout_2weeks", "#data_all", "#readout_all", "#readout-friends",
	"#readout-shame", "#hall-of-shame-content", "#friends"
];
    for (i = 0; i < elements.length; i++) {
        if (elements[i] === fade1 || elements[i] === fade2) {
            elements.splice(i, 1);
        }
    }
	
	for (i = 0; i < elements.length; i++) {
		$(elements[i]).css("display", "none");
	}
	
	$(fade1).fadeIn("slow");
	$(fade2).fadeIn("slow");
}

function hallOfShame() {
	$("#shame-tab").click(function() {
		displayElements("#hall-of-shame-content", "#readout-shame");
	});
}

function showFriends() {
	$("#friends-tab").click(function() {
		displayElements("#readout-friends", "#friends");
	});
}

function showDonut_2weeks(data) {
	displayElements("#readout_2weeks", "#donut_2weeks");
	options = {animationSteps: 70, animationEasing: "easeOutExpo"};
	var ctx = $("#donut-chart_2weeks").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Doughnut(data, options);
}

function showDonut_10(data) {
	displayElements("#readout_10", "#donut_10");
	options = {animationSteps: 70, animationEasing: "easeOutExpo"};
	var ctx = $("#donut-chart_10").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Doughnut(data, options);
}

function showDonut_20(data) {
	displayElements("#readout_20", "#donut_20");
	options = {animationSteps: 70, animationEasing: "easeOutExpo"};
	var ctx = $("#donut-chart_20").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Doughnut(data, options);
}

function showLine_2weeks(data) {
	displayElements("#readout_2weeks", "#line_2weeks");
	options = {scaleFontColor: "#FFFFFF"};
	var ctx = $("#line-chart_2weeks").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Line(data, options);
}

function showLine_10(data) {
	displayElements("#readout_10", "#line_10");
	options = {scaleFontColor: "#FFFFFF"};
	var ctx = $("#line-chart_10").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Line(data, options);
}

function showLine_20(data) {
	displayElements("#readout_20", "#line_20");
	options = {scaleFontColor: "#FFFFFF"};
	var ctx = $("#line-chart_20").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Line(data, options);
}

function showBar_2weeks(data) {
	displayElements("#readout_2weeks", "#bar_2weeks");
	options = {scaleFontColor: "#FFFFFF"};
	var ctx = $("#bar-chart_2weeks").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Bar(data, options);
}

function showBar_10(data) {
	displayElements("#readout_10", "#bar_10");
	options = {scaleFontColor: "#FFFFFF"};
	var ctx = $("#bar-chart_10").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Bar(data, options);
}

function showBar_20(data) {
	displayElements("#readout_20", "#bar_20");
	options = {scaleFontColor: "#FFFFFF"};
	var ctx = $("#bar-chart_20").get(0).getContext("2d");
	var myDoughnutChart = new Chart(ctx).Bar(data, options);
}

function showList_2weeks() {
	displayElements("#readout_2weeks", "#data_2weeks");
}

function showList_10() {
	displayElements("#readout_10", "#data_10");
}

function showList_20() {
	displayElements("#readout_20", "#data_20");
}

function showList_all() {
	displayElements("#readout_all", "#data_all");
}

function getFriendId() {
	$(".friend-avatar").click(function () {
		var alt = $(this).attr("alt");
		var top = $(window).scrollTop();
		console.log(top);
		$("#hidden-steamid").val(alt);
		$("#hidden-form").submit();
		$("#loading-dimmer").css("top", top).fadeIn("slow");
	});
}

function tabExpand() {
	$("#stats-tab").hover(
		function() {
			$(this).animate({
				"width" : "125px",
				"left" : "-95px"
			}, 10, function () {
				$("#stats-tab-text").fadeIn("slow");
			});
		},
		function() {
			$(this).animate({
				"width" : "30px",
				"left" : "0"
			}, 10, function () {
				$("#stats-tab-text").css("display", "none");
			});
		}
	);
	$("#friends-tab").hover(
		function() {
			$(this).animate({
				"width" : "125px",
				"left" : "-95px"
			}, 10, function () {
				$("#friends-tab-text").fadeIn("slow");
			});
		},
		function() {
			$(this).animate({
				"width" : "30px",
				"left" : "0"
			}, 10, function () {
				$("#friends-tab-text").css("display", "none");
			});
		}
	);
	$("#shame-tab").hover(
		function() {
			$(this).animate({
				"width" : "145px",
				"left" : "-115px"
			}, 10, function () {
				$("#shame-tab-text").fadeIn("slow");
			});
		},
		function() {
			$(this).animate({
				"width" : "30px",
				"left" : "0"
			}, 10, function () {
				$("#shame-tab-text").css("display", "none");
			});
		}
	);
}