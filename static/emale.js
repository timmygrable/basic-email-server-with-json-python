function populateInbox() {
    $.get("ajax_getinbox",function(inbox,status) {
	$("#ajax_table1").find("tbody").detach();
	$("#ajax_table1").append(
	    $.map(inbox,function(emale2,index) {
		result = "<tr>" +
		    "<td class='user'>"+ emale2.userid + "</td>" +
		    "<td class='subject'>"+ emale2.subject + "</td>" +
		    "<td class='message'><b> Click show to View Message </b> </td>" +
		    "<td><button type='button' class='showbutton' value="+emale2.val+">show</button></td>" +
		    "<td><button type='button' class='deletebutton' value="+emale2.val+">delete</button></td>" +
		    "<tr>"
		return result;
	    }).join());

	$(".showbutton").click(function(e) {
	    val = $(this).val();
	    $.get("ajax_getmessage?val="+val,function(emale2,status) {
		$(e.target.parentElement).siblings(".message")[0].innerHTML = emale2[0].message;
	    });
	    
	});

	$(".deletebutton").click(function(e) {
	    val = $(this).val();
	    $.get("ajax_deleteinbox?val="+val,function(emale2,status) {
		populateInbox()
	    });
	});
	
    });
}
function populateOutbox() {
     $.get("ajax_getoutbox",function(outbox,status) {
        $("#ajax_table2").find("tbody").detach();
	$("#ajax_table2").append(
	    $.map(outbox,function(emale2,index) {
		result = "<tr>"+
		    "<td class='user'>"+ emale2.sentto + "</td>" +
		    "<td class='subject'>"+ emale2.subject + "</td>" +
		    "<td class='message'><b> Click show to View Message </b></td>" +
		    "<td><button type='button' class='showbutton' value="+emale2.val+"> show </button></td>" +
		    "<td><button type='button' class='deletebutton' value="+emale2.val+"> delete </button></td>"+
		    "<tr>"
		return result;
	    }).join());


	$(".showbutton").click(function(e) {
	    val = $(this).val();
	    $.get("ajax_getmessage?val="+val,function(emale2,status){
		$(e.target.parentElement).siblings(".message")[0].innerHTML = emale2[0].message;
	    });
	    
	});
	 

	 $(".deletebutton").click(function(e) {
	     val= $(this).val();
	     $.get("ajax_deleteoutbox?val="+val,function(emale2,status) {
		 populateOutbox()
	     });
	 });
	 

     });


}

$(document).ready(function() {
    $("#ajax_form").submit(function(e) {
	e.preventDefault();
	populateInbox();
	populateOutbox();
    });
    populateInbox();
    populateOutbox();

});
