
var urlUsers = "/listURL";
function initTableData() {
    $.get(urlUsers, function(responseData) {
    	var modifiedUsers = responseData.map(eachUser => {
    		return {
    			stt: eachUser.stt,
    			url: eachUser.url,
                email: eachUser.email,
  				time: eachUser.time,
  				active_key: eachUser.active_key,
  				path_img: eachUser.path_img,
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
<<<<<<< HEAD
                defaultContent: '<button onclick="details();" type="button" title="Details" id="btnDetails" class="btn btn-rounded btn-outline-primary" data-toggle="modal" data-target="#ModalDetails"><i class="fa fa-eye-slash" aria-hidden="true"></i></button> <button onclick="createActiveKey();" title="Create Key" type="button" id="btnDelete" class="btn btn-rounded btn-outline-primary"><i class="fa fa-key" aria-hidden="true"></i></button> <button onclick="deleteitem();" type="button" title="Delete" id="btnDelete" class="btn btn-rounded btn-outline-danger"><i class="fa fa-trash"></button>',
=======
                defaultContent: '<button onclick="details();" type="button" id="btnDetails" class="btn btn-rounded btn-outline-primary" data-toggle="modal" data-target="#ModalDetails"><i class="fa fa-eye-slash" aria-hidden="true"></i></button> <button onclick="createActiveKey();" type="button" id="btnDelete" class="btn btn-rounded btn-outline-primary"><i class="fa fa-key" aria-hidden="true"></i></button> <button onclick="deleteitem();" type="button" id="btnDelete" class="btn btn-rounded btn-outline-danger"><i class="fa fa-trash"></button>',
>>>>>>> e3b46280aed34928603577d7a12b04d5c502a226
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
});

function details(){
<<<<<<< HEAD
=======
	var table = $('#urls').DataTable();
>>>>>>> e3b46280aed34928603577d7a12b04d5c502a226
	$('#urls tr').on( 'click', 'button', function (){
		var data = table.row( $(this).parents('tr') ).data();
		var path_img = data['path_img']
		$('#show_url').append(data['url']);
		$('#show_email').append(data['email']);
		$('#show_activekey').append(data['active_key']);	
		$('#show_img').append('<img class="card-img-top img-fluid" src="../static/images/'+path_img+'.png" alt="URL is not captured!">')	
	});
}

function deleteitem() {
    $('#urls tr').on( 'click', 'button', function () {
        var data = table.row( $(this).parents('tr') ).data();
		$.ajax({
			url: '/deleteURL',
			data: {'url':data['url']},
			type: 'POST',
			success: function(res) {
				if(res == "OKE"){
					alert("Delete successful!");
					location.reload();
				}else if (res == "Null"){
					alert("Bad data!");
					location.reload();
				}else{
					alert("URL not exist!")
				}
			},
			error: function(error) {
				console.log(error);
			}
		});
    } );
}

function createActiveKey() {
    $('#urls tr').on( 'click', 'button', function () {
        var data = table.row( $(this).parents('tr') ).data();
		$.ajax({
			url: '/createAgent',
			data: {'url':data['url']},
			type: 'POST',
			success: function(res) {
				if(res == "OKE"){
					alert("Generate Active Key Successful. Key sent your email!");
					location.reload();
				}else if (res == "Null"){
					alert("Bad data!");
					location.reload();
				}else{
					alert("URL invalid!")
				}
			},
			error: function(error) {
				console.log(error);
			}
		});
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
				alert("Bad data!");
				location.reload();
			}else{
				alert("URL existed. Please try again!");
			}
<<<<<<< HEAD
=======
			console.log(res);
>>>>>>> e3b46280aed34928603577d7a12b04d5c502a226
		},
		error: function(error) {
			console.log(error);
		}
	});
});