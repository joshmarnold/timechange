$(document).ready(function(){
    $(".alerts").click(function(){
        //window.location.href = "/loadFiles";

        window.location.href = Flask.url_for("alerts");
    });
});
