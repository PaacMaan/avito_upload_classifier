function readURL(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap').hide();

      $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').show();

      $('.image-title').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

    // make an ajax call to predict the image class

    var form = new FormData($("#upload-file")[0]);
    form.append('ad_category', $("#ad_category option:selected").val())

    var settings = {
      "async": true,
      "crossDomain": true,
      "url": window.location.href + "upload",
      "method": "POST",
      "headers": {
        "cache-control": "no-cache",
        "postman-token": "7002d400-f12f-22a6-f94d-5e9369488293"
      },
      "processData": false,
      "contentType": false,
      "mimeType": "multipart/form-data",
      "data": form
    }

    $.ajax(settings).done(function (response) {
        var json_result = JSON.parse(response);
        var predicted_classe = json_result['class'];
        var categories_matched = json_result['categories_matched']
        if (categories_matched == true) {
            swal("Good job!", "you choose the right category"+predicted_classe, "success")
        }else{
            classes = {0: 'laptop', 1: 'phone'}
            val = val2key(predicted_classe, classes)
            $("#ad_category option[value='"+val+"']")[0].selected = true;
            swal("Ooops", "Are you sure the ad category is about "+predicted_classe+" !!", "error")
        }
        
        console.log(response);
    });
  } else {
    removeUpload();
  }
}


function val2key(val,array){
    for (var key in array) {
        if(array[key] == val){
            return key;
        }
    }
 return false;
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.image-upload-wrap').show();
}
$('.image-upload-wrap').bind('dragover', function () {
		$('.image-upload-wrap').addClass('image-dropping');
	});
	$('.image-upload-wrap').bind('dragleave', function () {
		$('.image-upload-wrap').removeClass('image-dropping');
});