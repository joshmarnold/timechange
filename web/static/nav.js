$(document).ready(function(){
    $("#home").click(function(){
        window.location.href = "/home";
        // Flask.url_for("home");
    });

    $("#loadFiles").click(function(){
        window.location.href = "/loadFiles";
        // Flask.url_for("loadFiles");
    });

    $("#transformData").click(function(){
        window.location.href = "/transformData";
        // Flask.url_for("transformData");
    });

    $("#FFTPreview").click(function(){
        //window.location.href = "/FFTPreview";
        window.location.href = Flask.url_for("FFTPreview");
    });

    $("#configure").click(function(){
        //window.location.href = "/configure";
        window.location.href = Flask.url_for("configure");
    });

    $("#results").click(function(){
        //window.location.href = "/results";
        window.location.href = Flask.url_for("results");
    });
});
