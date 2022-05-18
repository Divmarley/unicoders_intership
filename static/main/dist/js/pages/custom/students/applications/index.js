const getDataTable = (url=$(".table-responsive").data('href')) => {
    $.ajax({
        url: url,
        type: "GET",
        success: function(response){
            $(".table-responsive").html(response);
        },
        error: function(response){
            console.log(JSON.stringify(response));
        }
    });
} 
getDataTable($(".table-responsive").data('href'));
 

$("#formAddNew").on("submit", function(e){
    e.preventDefault();
    e.stopPropagation(); 
    var $this = $(this);
    
        $('.btnAddNew').html('<i class="fa fa-spinner fa-spin"></i> ADDING NEW...').attr('disabled', true);
        let data = $this.serialize();
        console.log(data); 
        $.ajax({
            url: $this.attr('action'),
            type: "POST",
            dateType: "json",
            data: data,
            success: function(response){
                if(response.message=='success'){
                    swal({
                        title: "Added",
                        text: "New Application added successful",
                        type: "success",
                        confirmButtonClass: "btn-sm btn-success",
                        confirmButtonText: "OKAY",
                        closeOnConfirm: true
                        },
                    function(){
                        getDataTable();
                        $("#formAddNew input:text").val("");
                        // $("#formAddNew option[name='name']").focus();
                        $("#exampleModal").modal('hide');
                    });
                }else{
                    swal("Error", response.message.cv, "warning");
                   
                }
                $('.btnAddNew').html('<i class="fa fa-plus-circle"></i> ADD NEW').attr('disabled', false);
            },
            error: function(response){
                // console.log(JSON.stringify(response))
                console.log('something wrong with request')
                $('.btnAddNew').html('<i class="fa fa-plus-circle"></i> ADD NEW').attr('disabled', false);
            }
        });
 
    return false;
});
 
