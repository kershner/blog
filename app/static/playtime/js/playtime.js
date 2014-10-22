function playtime() {
	messageExists();
    showForm();
    showAbout();
    showFindID();
    closeFindID();
    closeAbout();
}

function playtimeResults(data1, data2, data3) {
	resultsFadeIn();
	hiddenMenu();
	showDonut(data1);
	showBar(data2);
	showLine(data3);
	showList();
}

function messageExists() {
	if ($(".message").length > 0) {
		$("#welcome-header, #big-logo, #slogan, #buttons, #footer, #form").fadeIn("fast");		
		$("#welcome-header").css("margin-top", "25px");
		$("#about-content").css("top", "25px");
		$(".select-box").customSelect();		
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

function showForm() {
	$("#get-started").one("click", function() {
		$("#form").fadeIn("slow", "linear");		
		$(".select-box").customSelect();
		$("#welcome-header").css("margin-top", "25px");
		$("#about-content").css("top", "25px");
	});
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
	}, 400);
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