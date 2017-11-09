$(document).ready(function(){
    var idx = 0;
    var data = {};



    $("#checkall").click(function () {
        if ($("#mytable #checkall").is(':checked')) {
            $("#mytable input[type=checkbox]").each(function () {
                $(this).prop("checked", true);
            });
        } else {
            $("#mytable input[type=checkbox]").each(function () {
                $(this).prop("checked", false);
            });
        }
    });
    var end = null;

    $('.checkthis').click(function(e){
        //clear the lab
        if($(this).val()==1){
            $(this).parents('tr').children('td').eq(3).remove();
            $(this).removeAttr("value");
            //remove from json obj
            var key_temp = $(this).parents('tr').children('td').eq(2).text();
            for(var id in data){
                for(var key in data[id]){
                    if(key == 'file_name'){
                        if(data[id][key]==key_temp){
                            delete data[id];

                        }
                    }
                }
            }
            console.log( JSON.stringify(data) );
        }



        if(e.shiftKey){
            if(!end){
                end = this;
                return false;
            }

            var first = $(this).parents('tr').children('td').eq(1).text();
            var last = $(end).parents('tr').children('td').eq(1).text();

            //check the boxes between first and last
            $('.checkthis').slice(Math.min(first, last), Math.max(first, last)-1).prop("checked", end.checked);
        }

        end = this;
    });

    $("[data-toggle=tooltip]").tooltip();

    $(".mysubmit").click(function(){
        var checked_box = $('#mytable').find('input:checked');
        var num_files = checked_box.length;

        //Label
        var lable_val = $('.labelVal').val();
        var total_files = $("#mytable > tbody > tr").length;

        console.log("WERE in");

        if(!lable_val){
          console.log("HEREEEEEE");
          Materialize.toast('Uh oh, you forgot to add a label', 4000);
          return;
        }
        //alert(num_files+":"+Object.keys(data).length);
        if(num_files == Object.keys(data).length){
            Materialize.toast({{'Uh oh'}}, 4000, );
            return false;
        }

        if(idx >= total_files){
            //alert("Already label all the files");
            //return false;
        }
        //for loop each selected files
        $(checked_box).each(function(){
            var $td = $(this).parents('tr').children('td');

            //File name
            var file_name = $td.eq(2).text();


            //show label in html page
            if(file_name){
                //unlabed files
                if($(this).val()!=1){
                    var applabel = "<td>"+lable_val+"</td>"
                    $(this).parents('tr').append(applabel);
                    data[idx]={'file_name':file_name,
                        'label': lable_val};
                    idx++;
                    $(this).attr("value", 1);
                    //$(this).attr("disabled", true);
                }
            }

            console.log( JSON.stringify(data) );
        });
    });
});
