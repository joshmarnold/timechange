$(document).ready(function(){

  $(".submitjson").click(function(){
    console.log("HELLO");
    var ret_json = [];

    var table = document.getElementById("mytable"); // grab table

    var len = table.rows.length - 1; // grab # of labeled rows

    for(var i = 1; i < len + 1; i++) {

      var fn = mytable.rows[i].cells[2].innerHTML;
      var label = mytable.rows[i].cells[3].innerHTML;

      var x = {"file_name":fn,"label":label};

      ret_json.push(x);
    }

    var x = 1;

    $.ajax({
      data: JSON.stringify(ret_json),
      dataType: 'application/json',
      url: '/getjson',
      type: 'POST',
      contentType: 'application/json; charset=utf-8',
      // success: function (result) {
      //   alert(result);
      // },
      // failure: function (errMsg) {
      //   alert(errMsg);
      // }
    });
  });
});











































// $(document).ready(function(){
//   var idx = 0;
//   var data = {};
//
//
//
//   $("#checkall").click(function () {
//     if ($("#mytable #checkall").is(':checked')) {
//       $("#mytable input[type=checkbox]").each(function () {
//         $(this).prop("checked", true);
//       });
//     } else {
//       $("#mytable input[type=checkbox]").each(function () {
//         $(this).prop("checked", false);
//       });
//     }
//   });
//   var end = null;
//
//
//
//   $('#getlabel').click(function() {
//     if($(this).val()==1){
//       $(this).parents('tr').children('td').eq(3).remove();
//       $(this).removeAttr("value");
//       //remove from json obj
//       var key_temp = $(this).parents('tr').children('td').eq(2).text();
//       for(var id in data){
//         for(var key in data[id]){
//           if(key == 'file_name'){
//             if(data[id][key]==key_temp){
//               delete data[id];
//
//             }
//           }
//         }
//       }
//       console.log( JSON.stringify(data) );
//       $.ajax({
//         type: 'POST',
//         contentType: 'application/json',
//         data: JSON.stringify(data),
//         dataType: 'json',
//         url: '/getjson',
//         success: function () {
//
//           Materialize.toast("success", 4000);
//         },
//         error: function(error) {
//           console.log(error);
//         }
//       });
//     };
//   });
//
//
//
//
//   // if(e.shiftKey){
//   //   if(!end){
//   //     end = this;
//   //     return false;
//   //   }
//
//   //   var first = $(this).parents('tr').children('td').eq(1).text();
//   //   var last = $(end).parents('tr').children('td').eq(1).text();
//   //
//   //   //check the boxes between first and last
//   //   $('.checkthis').slice(Math.min(first, last), Math.max(first, last)-1).prop("checked", end.checked);
//   // }
//
//   end = this;
// });
//
// $("[data-toggle=tooltip]").tooltip();
//
// $(".mysubmit").click(function(){
//   var checked_box = $('#mytable').find('input:checked');
//   var num_files = checked_box.length;
//
//   //Label
//   var lable_val = $('.labelVal').val();
//   var total_files = $("#mytable > tbody > tr").length;
//
//   if(!lable_val){
//     Materialize.toast('Uh oh, you forgot to add a label', 4000);
//     return false;
//   }
//   //alert(num_files+":"+Object.keys(data).length);
//   if(num_files == Object.keys(data).length){
//     Materialize.toast('Uh oh', 4000 );
//     return false;
//   }
//
//   if(idx >= total_files){
//     //alert("Already label all the files");
//     //return false;
//   }
//   //for loop each selected files
//   $(checked_box).each(function(){
//     var $td = $(this).parents('tr').children('td');
//
//     //File name
//     var file_name = $td.eq(2).text();
//
//
//     //show label in html page
//     if(file_name){
//       //unlabed files
//       if($(this).val()!=1){
//         var applabel = "<td>"+lable_val+"</td>"
//         $(this).parents('tr').append(applabel);
//         data[idx]={'file_name':file_name,
//         'label': lable_val};
//         idx++;
//         $(this).attr("value", 1);
//         //$(this).attr("disabled", true);
//       }
//     }
//
//     console.log( JSON.stringify(data) );
//   });
// });
