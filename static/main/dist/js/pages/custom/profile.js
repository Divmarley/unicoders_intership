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



$("#formChangePassword").on("submit", function(e){
    e.preventDefault();
    e.stopPropagation();
    var valid = true;
    var $this = $(this);
    $('#formChangePassword input:password').each(function() {
        let $this = $(this);
        if($this.attr('id')=='password'){
            if($this.val().length<6){
                valid = false;
                $this.parents('.validate').find('.mySpan').text('Password field must be more than 6 characters');
            }
        }
        if(!$this.val()) {
            valid = false;
            $this.parents('.validate').find('.mySpan').text('The '+$this.attr('id').replace(/[\_]+/g, ' ')+' field is required');
        }
    });

    if($("#password_confirmation").val()!=$("#password").val()){
        valid = false;
        $("#password_confirmation").parents('.validate').find('.mySpan').text('Password does not match');
    }

    if(valid) {
        $('.btnChangePassword').html('<i class="fa fa-spinner fa-spin"></i> CHANGING PASSWORD...').attr('disabled', true);
        let data = $this.serialize();
        $.ajax({
            url: $this.attr('action'),
            type: "POST",
            dataType: 'json',
            data: data,
            success: function(response){
                if(response.message=='success'){
                    swal({
                        title: "Changed",
                        text: "Your password is changed successful",
                        type: "success",
                        confirmButtonClass: "btn-success btn-sm",
                        cancelButtonClass: "btn-sm",
                        confirmButtonText: "Okay",
                        closeOnConfirm: true
                        },
                    function(){
                        $("#formChangePassword #current_password").val('');
                        $("#formChangePassword #password").val('');
                        $("#formChangePassword #password_confirmation").val('');
                    });
                }else{
                    let text = "";
                    $.map( response, function( val, i ) {
                        let old = (val.old_password==undefined)? '': val.old_password;
                        let newp = (val.new_password2==undefined)? '': val.new_password2;
                        text+=old+'\n'+newp;
                    });

                    $("#msgContainer").text(text);
                    $("#formChangePassword #current_password").val('').focus();
                    $("#formChangePassword #password").val('');
                    $("#formChangePassword #password_confirmation").val('');
                }
                $('.btnChangePassword').html('<i class="fa fa-refresh"></i> CHANGE PASSWORD').attr('disabled', false);
            },
            error: function(response){
                console.log('something wrong with request')
                $('.btnChangePassword').html('<i class="fa fa-refresh"></i> CHANGE PASSWORD').attr('disabled', false);
            }
        });
    }
    return false;
});
  
  $("#formChangePassword input").on('input', function(){
    if($(this).val()!=''){
        $(this).parents('.validate').find('.mySpan').text('');
    }else{ $(this).parents('.validate').find('.mySpan').text('The '+$(this).attr('name').replace(/[\_]+/g, ' ')+' field is required'); }
  });

