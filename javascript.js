$(document).ready(function() {
  $(".file_text input").change(function(){
      var val = $(this).val();
      $("#selected_file").html(val.replace("C:\\fakepath\\", "File Selected: "));
  });
});