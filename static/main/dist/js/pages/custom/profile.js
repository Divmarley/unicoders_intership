$("#createSocialLink").on("submit", function(e){
    e.stopPropagation();
    e.preventDefault();
    var $this = $(this);
    var valid = true;
    $('#createSocialLink input').each(function() {
        let $this = $(this);
        
        if(!$this.val()) {
            valid = false;
            $this.parents('.validate').find('.mySpan').text('The '+$this.attr('name').replace(/[\_]+/g, ' ')+' field is required');
        }
    });

    if(valid){
        $("#createSocialLink .btnsubmit").html('<i class="fa fa-spin fa-spinner"></i> Submitting...').attr('disabled',true);
        let data = $this.serialize();
        console.log(data);
        // alert(".bjdsbfjbsd")
        $.ajax({
            url: $("#createSocialLink").attr("action"),
            type: "POST",
            dateType: "json",
            data: data,
            // headers: { 'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val() },
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
              },
            success: function(resp){
                if(resp.message==='success'){
                    swal({
                        title: "Success",
                        text: `Zone is created successful`,
                        type: "success",
                        showCancelButton: false,
                        confirmButtonClass: "btn-sm text-primary",
                        confirmButtonText: "Okay",
                        },
                    function(){
                        window.location.reload();
                    });
                }else{
                    if(resp.message.name){
                        swal('Error', `${resp.message.name}`, 'warning');
                    }else{
                        swal('Error', `${resp.message}`, 'warning');
                    }
                }
                $("#createSocialLink .btnsubmit").html('Submit <i class="icon-paperplane ml-2"></i>').attr('disabled',false);
            },
            error: function(resp){
                console.log('something wrong with request')
                $("#createSocialLink .btnsubmit").html('Submit <i class="icon-paperplane ml-2"></i>').attr('disabled',false);
            }
        });
    }
    return false;
});
