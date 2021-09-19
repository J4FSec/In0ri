var urlSetting = "/listSetting";
function initTableData() {
	var smtp;
	var telegram;
	var smtp_address;
	var smtp_server;
	var first_name;
	var title;
    $.get(urlSetting, function(responseData) {
    	responseData.forEach(function(item, index, array) {
			smtp = item.smtp
			telegram = item.telegram
		});
		if (typeof smtp !== 'undefined'){
			smtp.forEach(function(item, index, array){
				smtp_address = item.smtp_address
				smtp_server = item.smtp_server
			});
		};
		
		if (typeof smtp !== 'undefined'){
			telegram.forEach(function(item, index, array){
				first_name = item.first_name
				title = item.title
			});
		};

		let htmlsmtp = '';
		if (typeof smtp === 'undefined' || smtp.length == 0){
			let htmlSegment = `
			<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#ModalAddSMTP">
				Add SMTP
			</button>
			<div class="alert alert-outline-primary alert-dismissible fade show">No Setting created yet. Let's create one!</div>
			`;
			htmlsmtp += htmlSegment;
			let containersmtp = document.querySelector('.SMTP');
			containersmtp.innerHTML = htmlsmtp;
		} else {
			let htmlSegment = `
			<div class="card">
				<div class="card-header">
					<h4 class="card-title">Details</h4>
				</div>
				<div class="card-body">
					<div class="table-responsive">
						<table class="table table-bordered verticle-middle table-responsive-sm">
							<thead>
								<tr>
									<th scope="col">Host</th>
									<th scope="col">Email</th>
									<th scope="col">Action</th>
								</tr>
							</thead>
							<tbody>
								<tr>
									<td><span id="smtp_server"></span></td>
									<td><span id="smtp_address"></span></td>
									</td>
									<td>
									<button type="button" title="Edit" class="btn btn-rounded btn-outline-primary"><i class="fa fa-pencil color-muted" aria-hidden="true" data-toggle="modal" data-target="#ModalAddSMTP"></i></button> <button onclick="deletesmtp();" type="button" title="Delete" class="btn btn-rounded btn-outline-danger"><i class="fa fa-trash" aria-hidden="true"></i></button>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
			`
			htmlsmtp += htmlSegment;
			let containersmtp = document.querySelector('.SMTP');
			containersmtp.innerHTML = htmlsmtp;
			$('#smtp_server').append(smtp_server);
			$('#smtp_address').append(smtp_address);
		}
		

		let htmlbot = '';
		if (typeof telegram === 'undefined' || telegram.length == 0){
			let htmlSegment = `
			<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#ModalAddBOT">
			Add Telegram
			</button>
			<div class="alert alert-outline-primary alert-dismissible fade show">No Setting created yet. Let's create one!</div>
			`;
			htmlbot += htmlSegment;
			let containerbot = document.querySelector('.BOT');
    		containerbot.innerHTML = htmlbot;
		} else {
			let htmlSegment = `
			<div class="card">
				<div class="card-header">
					<h4 class="card-title">Details</h4>
				</div>
				<div class="card-body">
					<div class="table-responsive">
						<table class="table table-bordered verticle-middle table-responsive-sm">
							<thead>
								<tr>
									<th scope="col">Chanel</th>
									<th scope="col">Bot</th>
									<th scope="col">Action</th>
								</tr>
							</thead>
							<tbody>
								<tr>
									<td><span id="title"></span></td>
									<td><span id="first_name"></span></td>
									</td>
									<td>
									<button type="button" title="Edit" class="btn btn-rounded btn-outline-primary" data-toggle="modal" data-target="#ModalAddBOT"><i class="fa fa-pencil color-muted" aria-hidden="true"></i></button> <button onclick="deletetelegram();" type="button" title="Delete" class="btn btn-rounded btn-outline-danger"><i class="fa fa-trash" aria-hidden="true"></i></button>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
			`
			htmlbot += htmlSegment;
			let containerbot = document.querySelector('.BOT');
    		containerbot.innerHTML = htmlbot;
			$('#first_name').append(first_name);
			$('#title').append(title);
		}
        $.noConflict();
    }).fail(function() {
    	alert( "Cannot get data from URL" );
    });
}

function deletesmtp() {
	$.ajax({
		url: '/deleteSetting',
		data: '&bot=smtp',
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
}


function deletetelegram() {
	$.ajax({
		url: '/deleteSetting',
		data: '&bot=telegram',
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
}


$('#smtp').submit(function(e) {
	e.preventDefault();
	let smtp_server = $('#smtp_server').val();
	let smtp_address = $('#smtp_address').val();
	let smtp_password = $('#smtp_password').val();
	$.ajax({
		url: '/setting',
		data: '&bot=smtp' + '&smtp_server='+smtp_server+ '&smtp_address='+smtp_address+ '&smtp_password='+smtp_password,
		type: 'POST',
		success: function(res) {
			if(res == "OKE"){
				alert("Setting SMTP Server successful!");
				location.reload();
			}else if (res == "Null"){
				alert("Bad data!");
				location.reload();
			}
		},
		error: function(error) {
			console.log(error);
		}
	});
});

$('#btnAddBOT').click(function(e) {
	e.preventDefault();
	let chat_id = $('#chat_id').val();
	let token = $('#token').val();
	$.ajax({
		url: '/setting',
		data: '&bot=telegram' + '&token=' + token+ '&chat_id=' + chat_id,
		type: 'POST',
		success: function(res) {
			if(res == "OKE"){
				alert("Setting Telegram Chanel successful!");
				location.reload();
			}else if (res == "Null"){
				alert("Bad data!");
				location.reload();
			}else{
				alert("Token or Chat ID invalid!");
			}
		},
		error: function(error) {
			console.log(error);
		}
	});
});

$(document).ready(function (){
	initTableData();
});