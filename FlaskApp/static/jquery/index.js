var table;
var editor;
var urlUsers = "/listURL";
function initTableData() {
    $.get(urlUsers, function(responseData) {
    	var modifiedUsers = responseData.map(eachUser => {
    		return {
    			stt: eachUser.stt,
    			url: eachUser.url,
                email: eachUser.email,
  				time: eachUser.time,
    		};
    	});
        $.noConflict();
    	table = $('#urls').DataTable({
    	"processing": true,
		columnDefs: [
			{
				className: 'text-center', targets: [0, 1, 2, 3]
			}
		  ],
    	data: modifiedUsers,
    	columns:[
    		{ data: 'stt' },		
    		{ data: 'url' },
    		{ data: 'email' },
    		{ data: 'time' },
			{
                data: null,
                className: "dt-center editor-delete",
                defaultContent: '<button onclick="createActiveKey();" type="button" id="btnDelete" class="btn btn-rounded btn-outline-primary"><i class="fa fa-eye-slash" aria-hidden="true"></i></button>',
                orderable: false
            },
            {
                data: null,
                className: "dt-center editor-delete",
                defaultContent: '<button onclick="deleteitem();" type="button" id="btnDelete" class="btn btn-rounded btn-outline-danger"><i class="fa fa-trash"></button>',
                orderable: false
            }
    	]
    	});
    }).fail(function() {
    	alert( "Cannot get data from URL" );
    });


}

$(document).ready(function (){
	initTableData();


	$("#btnReloadData").on("click", function(){
		//alert("reload data...")
		table.ajax.reload();
	});
});

function deleteitem() {
    var table = $('#urls').DataTable();
 
    $('#urls tr').on( 'click', 'button', function () {
        var data = table.row( $(this).parents('tr') ).data();
        // alert( data['url'] +"'s email is: "+ data['email'] );
		$.ajax({
			url: '/deleteURL',
			data: {'url':data['url']},
			type: 'POST',
			success: function(res) {
				if(res == "OKE"){
					alert("Delete successful!");
					// window.location.href = '/';
					location.reload();
				}else if (res == "Null"){
					alert("Exception data!");
					location.reload();
				}else{
					alert("URL not exist!")
				}
				console.log(res);
			},
			error: function(error) {
				console.log(error);
			}
		});
        // location.reload();

    } );

}

function createActiveKey() {
    var table = $('#urls').DataTable();
 
    $('#urls tr').on( 'click', 'button', function () {
        var data = table.row( $(this).parents('tr') ).data();
		$.ajax({
			url: '/createAgent',
			data: {'url':data['url']},
			type: 'POST',
			success: function(res) {
				if(res == "OKE"){
					alert("Generate Active Key Successful. Key sent your email!");
					// window.location.href = '/';
					location.reload();
				}else if (res == "Null"){
					alert("Exception data!");
					location.reload();
				}else{
					alert("URL not invalid!")
				}
				console.log(res);
			},
			error: function(error) {
				console.log(error);
			}
		});
        // location.reload();

    } );

}

$('#btnAdd').click(function(e) {
	e.preventDefault();
	$.ajax({
		url: '/register',
		data: $('form').serialize(),
		type: 'POST',
		success: function(res) {
			if(res == "OKE"){
				alert("Register moniter successful!");
				location.reload();
			}else if (res == "Null"){
				alert("Exception data!");
				location.reload();
			}else{
				alert("URL existed. Please try again!");
			}
			console.log(res);
			// alert("sussess");
		},
		error: function(error) {
			// alert("error");
			console.log(error);
			
		}
	});
	
});