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
 
