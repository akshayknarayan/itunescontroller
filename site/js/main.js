$(document).ready(function() {
	var auth = '';
	function getAuthKey() {
		var auth = '';
		for (var i=1;i<7;i++) {
			auth += $("#auth"+i).val();
		}
		return auth;
	}
	function getPlaylists(callback) {
		var req = $.ajax("./app?auth="+auth+"&playlists");
		req.done(function(data, textStatus) {
			callback(data.substring(1,data.length-2).replace(/\'/g,"").replace(/-/g," ").split(","));
		});
	}
	function play(toplay, callback) {
		var req = $.ajax("./app?auth="+auth+"&play="+toplay);
		req.done(function(data) {
			callback();
		});
	}
	function pause(callback) {
		var req = $.ajax("./app?auth="+auth+"&pause");
		req.done(function(data) {
			callback();
		});
	}
	$("#auth1").on("input", function() {
		$("#auth2").focus();
	});
	$("#auth2").on("input", function() {
		$("#auth3").focus();
	});
	$("#auth3").on("input", function() {
		$("#auth4").focus();
	});
	$("#auth4").on("input", function() {
		$("#auth5").focus();
	});
	$("#auth5").on("input", function() {
		$("#auth6").focus();
	});
	$("#auth6").on("input", function() {
			$(".btn").focus();
	});
	$("#auth-panel .btn").click(function() {
		auth = getAuthKey();
		getPlaylists(function(playlists) {
			console.log("got playlists: "+playlists);
			$("#control-panel select").attr('size',playlists.length);
			for (var i=0;i<playlists.length;i++) {
				$("#control-panel select").append("<option>"+playlists[i]+"</option>");
			}
			$("#auth-panel").fadeOut(400, function() {
				$("#control-panel").fadeIn();
			});
		});
	});
	
	$("#play").click(function() {
		if ($("#control-panel select").val()) {
			var selected = $("#control-panel select").val();
			console.log("selected: "+selected);
			selected = selected[0].replace(/ /g,"-")
			play(selected, function() {
				$("#play").hide();
				$("#pause").show();
			});
		}
		else {
			$("#control-panel .alert").show();
			window.setTimeout(function() {
				$("#control-panel .alert").fadeOut();
			}, 2000);
		}
	});
	$("#pause").click(function() {
		pause(function() {
			console.log("paused");
			$("#pause").hide();
			$("#play").show();	
		});
	});
	
	$("#auth1").focus();
});