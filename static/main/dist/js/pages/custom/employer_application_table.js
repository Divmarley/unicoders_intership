$("#example23 tbody").on('click', '.btn_delete', function(e){

    e.preventDefault();
    e.stopPropagation();
    var $this = $(this);
    swal({
        title: "Sure to delete?",
        text: "This action is irreversible",
        type: "warning",
        showCancelButton: true,
        confirmButtonClass: "btn-danger btn-sm",
        cancelButtonClass: "btn-sm",
        confirmButtonText: "Yes, delete",
        closeOnConfirm: true
        },
    function(){
        $.ajax({
            url: $this.attr('href'),
            type: "GET",
            dataType: "json",
            success: function(response){
                if(response.message=='success'){
                    $this.parents('.record').fadeOut('slow', function(){
                        $this.parents('.record').remove();
                        getDataTable()
                    });
                }else{
                    console.log("something went wrong");
                }
            },
            error: function(response){
                console.log('something wrong with request')
            }
        });
    });
    return false;
});
 
$("#example23 tbody").on('click', '.ViewMyAppModalBtn', function(e){
    e.preventDefault();
    e.stopPropagation();
    var $this = $(this);
    $("#ViewMyAppModal .modal-title").text("Application for "+$this.parents('.record').find('td').eq(0).text());
    $("#ViewMyAppModal .quli").text($this.parents('.record').find('td').eq(1).text());
    $("#ViewMyAppModal .exprie").text($this.parents('.record').find('td').eq(2).text());
    $("#ViewMyAppModal .payment_budget").text($this.parents('.record').find('td').eq(3).text());
    $("#ViewMyAppModal .location").text($this.parents('.record').find('td').eq(4).text());
    $("#ViewMyAppModal .desciption").text($this.parents('.record').find('td').eq(5).text()); 
    $("#ViewMyAppModal .created_at").text($this.parents('.record').find('td').eq(6).text()); 
    $("#ViewMyAppModal").modal('show'); 
    return false;
    
});
    

     