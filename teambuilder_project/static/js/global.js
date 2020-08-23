$( document ).ready(function() {

  $('textarea').autogrow({onInitialize: true});


  //Cloner for infinite input lists
  $(".circle--clone--list").on("click", ".circle--clone--add", function(){
    var parent = $(this).parent("li");
    var copy = parent.clone();
    parent.after(copy);
    copy.find("input, textarea, select").val("");
    copy.find("*:first-child").focus();
  });

  $(".circle--clone--list").on("click", "li:not(:only-child) .circle--clone--remove", function(){
    var parent = $(this).parent("li");
    parent.remove();
  });

  // Adds class to selected item
  $(".circle--pill--list a").click(function() {
    $(".circle--pill--list a").removeClass("selected");
    $(this).addClass("selected");
  });

  // Adds class to parent div of select menu
  $(".circle--select select").focus(function(){
   $(this).parent().addClass("focus");
   }).blur(function(){
     $(this).parent().removeClass("focus");
   });

  // Clickable table row
  $(".clickable-row").click(function() {
      var link = $(this).data("href");
      var target = $(this).data("target");

      if ($(this).attr("data-target")) {
        window.open(link, target);
      }
      else {
        window.open(link, "_self");
      }
  });

  // Custom File Inputs
  var input = $(".circle--input--file");
  var text = input.data("text");
  var state = input.data("state");
  input.wrap(function() {
    return "<a class='button " + state + "'>" + text + "</div>";
  });


    // jquery-cropper
    $(function () {

        /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
        $("#id_avatar").change(function () {
            if (this.files && this.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $("#image").attr("src", e.target.result);
                    $('#modalCrop').modal('show')
                }
                reader.readAsDataURL(this.files[0]);
            }
        });

        /* SCRIPTS TO HANDLE THE CROPPER BOX */
        var $image = $("#image");
        var cropBoxData;
        var canvasData;
        $("#modalCrop").on("shown.bs.modal", function () {
            $image.cropper({
                viewMode: 1,
                aspectRatio: 1 / 1,
                minCropBoxWidth: 200,
                minCropBoxHeight: 200,
                zoomOnWheel: false,
                modal: true,
                ready: function () {
                    $image.cropper("setCanvasData", canvasData);
                    $image.cropper("setCropBoxData", cropBoxData);
                }
            });
        }).on("hidden.bs.modal", function () {
            cropBoxData = $image.cropper("getCropBoxData");
            canvasData = $image.cropper("getCanvasData");
            $image.cropper("destroy");
        });

        $(".js-zoom-in").click(function () {
            $image.cropper("zoom", 0.1);
        });

        $(".js-zoom-out").click(function () {
            $image.cropper("zoom", -0.1);
        });

        $(".js-rotate-clockwise").click(function () {
            $image.cropper("rotate", 11.25);
        });

        $(".js-rotate-counter-clockwise").click(function () {
            $image.cropper("rotate", -11.25);
        });

        $(".js-drag").click(function () {
            $image.cropper("setDragMode", "move");
        });

        /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
        $(".js-crop-and-upload").click(function () {
            var cropData = $image.cropper("getData");
            $("#id_x").val(cropData["x"]);
            $("#id_y").val(cropData["y"]);
            $("#id_height").val(cropData["height"]);
            $("#id_width").val(cropData["width"]);
            $("#id_rotate").val(cropData["rotate"]);
            $("#formUpload").submit();
        });
    });

});