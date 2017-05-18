/**
 * Created by David on 17.05.2017.
 */

let createDeleteButton = function (idAttribute, clickListener) {
	let button = document.createElement("i");
	button.className = "fa fa-trash-o text-danger rses-ab-d rses-ab-table";
	button.setAttribute(idAttribute.name, idAttribute.id);
	button.setAttribute('aria-hidden', 'true');
	button.addEventListener("click", clickListener);
	return button
};

let createEditButton = function (idAttribute, clickListener) {
	let button = document.createElement("i");
	button.className = "fa fa-pencil text-info rses-ab-i rses-ab-table";
	button.setAttribute(idAttribute.name, idAttribute.id);
	button.setAttribute('aria-hidden', 'true');
	button.setAttribute('data-toggle', 'modal');
	button.setAttribute('data-target', '#edit-modal');
	button.addEventListener("click", clickListener);
	return button
};


let notifySuccess = function (text) {
	let alert = document.createElement('div');
	alert.className = "alert alert-success alert-dismissable";
	let closeButton = document.createElement('a');
	closeButton.className = "close";
	closeButton.setAttribute('data-dismiss', 'alert');
	closeButton.setAttribute('aria-label', 'close');
	closeButton.innerHTML = '&times;';
	let strong = document.createElement('strong');
	strong.innerHTML = '<i class="fa fa-check" aria-hidden="true"></i> ';
	alert.appendChild(strong);
	alert.innerHTML += text;
	let alerts = document.getElementById('alerts');
	alert.appendChild(closeButton);
	alerts.appendChild(alert);
	setTimeout(function () {alert.style = 'display: none';}, 5000)
};