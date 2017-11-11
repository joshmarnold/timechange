$(document).ready(function(){
    $("#home").click(function(){
        //window.location.href = "/home";
        window.location.href = Flask.url_for("home");
    });

    $("#loadFiles").click(function(){
        //window.location.href = "/loadFiles";
        window.location.href = Flask.url_for("loadFiles");
    });

    $("#mytransfromData").click(function(){
        //window.location.href = "/transfromData";
        window.location.href = Flask.url_for("transfromData");
        //window.location.href = Flask.url_for("transfromData");
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
