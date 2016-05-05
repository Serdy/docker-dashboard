$(document).on("click", ".open-delhostDialog", function () {
     var myhostId = $(this).data('id');
     $(".modal-body #hostId").val( myhostId );
     console.log(myhostId);
});
