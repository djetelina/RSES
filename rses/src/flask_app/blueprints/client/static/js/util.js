/**
 * Created by David on 17.05.2017.
 */

let fetchRses = async (apiUrl, method) => {
	return fetch('/rses/api' + apiUrl, {credentials: "include", method: method})
		.then(res => {
			switch (res.status) {
				case 403:
					throw 'Unauthorized request';
				case 404:
					throw 'Not found';
				case 200: case 201: case 202:
					return res.json()
			}
			console.error(res);
			throw 'Unexpected error';
		})
		.then(out => {
			console.debug(method.toUpperCase() + ' ' + apiUrl + ' \n', out);
			return out
		})
		.catch(err => {
			notifyError(err);
			throw 'Stopping function execution'; // TODO I don't like JS
		});
};


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


let notifyBase = function (severity, icon, text) {
	let alert = document.createElement('div');
	alert.className = "alert alert-" + severity + " alert-dismissable";
	let closeButton = document.createElement('a');
	closeButton.className = "close";
	closeButton.setAttribute('data-dismiss', 'alert');
	closeButton.setAttribute('aria-label', 'close');
	closeButton.innerHTML = '&times;';
	let strong = document.createElement('strong');
	strong.innerHTML = '<i class="fa fa-' + icon + '" aria-hidden="true"></i> ';
	alert.appendChild(strong);
	alert.innerHTML += text;
	alert.appendChild(closeButton);
	let alerts = document.getElementById('alerts');
	alerts.appendChild(alert);
	setTimeout(function () {
		alert.style = 'display: none';
	}, 5000)
};


let notifySuccess = function (text) {
	notifyBase('success', 'check', text);
};

let notifyError = function (text) {
	notifyBase('danger', 'cross', text)
};
