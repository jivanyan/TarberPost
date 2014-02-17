$(document).ready(function(){
	
        $('#search-submit').click(function(){
                var sp = $('#sp').val();
                var ep = $('#ep').val();
                alert(sp+ep);
		$("#search_result").html("AAAAA");
		
		 $.ajax({
                	type: "GET",
                	url: "/patron/suggest_bids/",
                	data: {sp: sp, ep:ep },
                	success: function(response) {
                	      alert(response);
                	},
			error: function(jqXHR, textStatus, errorThrown) 
         		{
		              alert(errorThrown);
          		},
                	/*error: function(xhr) {
                	    alert("failure" + xhr.readyState + this.url);
                	},*/
                	dataType: 'html',
            	});		

	/*	$.ajax({
   			type: "post",
			url:"/patron/search_bids/",
    			data: {sp:sp, ep:ep},
			dataType : html
    			success:  function(response) {
                    		alert(response.msg);
                	},
			
			error: function(xhr) {
                    		alert("failure" + xhr.readyState + this.url);
                	},		
    			
		});*/
		
                /*$.get('/patron/suggest_bids/', {sp:sp, ep:ep}, function(data){
                        alert(data);
                        //$("#search_result").html(data);
                        });*/
         });
                       

});
