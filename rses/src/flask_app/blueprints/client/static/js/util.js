/**
 * Created by David on 17.05.2017.
 */

/**
 * Wrapped fetch for RSES API
 * @param apiUrl        URL to fetch from
 * @param method        HTTP Method to use
 * @returns {Object}    JSON response from the API
 */
const fetchRses = async (apiUrl, method) => {
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
};


/**
 * Fetches from RSES API and on error creates an error notification
 * @param apiUrl            URL to fetch from
 * @param method            HTTP Method to use
 * @returns {Object}        JSON response from the API
 */
const fetchRsesCatch = async (apiUrl, method) => {
	return fetchRses(apiUrl, method)
		.catch(err => {
			notifyError(err);
		});
};

/**
 * Creates a simple icon-button
 * @param idAttribute       An object of the id attribute containing id and name
 * @param clickListener     Function to be called
 * @param action            What action the button represents
 * @returns {Element}       The button
 */
const createActionButton = function (idAttribute, clickListener, action) {
	let button_class;
	let additional = "";
	switch(action) {
		case "edit":
			button_class = `fa fa-pencil text-info rses-ab-i rses-ab-table`;
			additional = `data-toggle="modal" data-target="#edit-modal"`;
			break;
		case "delete":
			button_class = `fa fa-trash-o text-danger rses-ab-d rses-ab-table`;
			break;
	}
	const templateHTML = `
		<i class="${button_class}" 
		${idAttribute.name}="${idAttribute.id}"
		aria-hidden="true"
		${additional}"></i>`;
	const button = htmlToElement(templateHTML);
	button.addEventListener("click", clickListener);
	return button
};

/**
 * Creates a success notification
 * @param text  Text to show
 */
const notifySuccess = function (text) {
	notifyBase('success', 'check', text);
};

/**
 * Creates an error notification
 * @param text  Text to show
 */
const notifyError = function (text) {
	notifyBase('danger', 'cross', text)
};

/**
 * Base for notification
 * @param severity  Notification severity
 * @param icon      Icon to use
 * @param text      Text to show
 */
const notifyBase = function (severity, icon, text) {
	const alertHTML = `
	<div class="alert alert-${severity} alert-dismissable">
		<strong><i class="fa fa-${icon}" aria-hidden="true"></i></strong> 
		${text}
		<a class="close" data-dismiss="alert" aria-label="close">&times</a>
	</div>
	`;
	const alert = htmlToElement(alertHTML);
	const alerts = document.getElementById('alerts');
	alerts.appendChild(alert);
	setTimeout(function () {
		alert.style = 'display: none';
	}, 5000)
};

/**
 * Element to show while something os loading
 * @returns {string}
 */
const tableLoading = function () {
	return `<tr><td colspan="2" align="center"><i class="text-info fa fa-refresh fa-spin fa-2x fa-fw"></i>
									<span class="sr-only">Loading...</span></td></tr>`;
};

const HTMLEntities = [
	['&amp', '&'],
	['&apos', '\''],
	['&lt', '<'],
	['&gt', '>'],
	['&nbsp', ' '],
	['&quot', '"']
];

/**
 * Decodes HTML
 * @param text      To decode
 * @returns {string}     Decoded
 */
const decodeHTML = function (text) {
	HTMLEntities.forEach(entity => {
		text = text.replace(new RegExp(entity[0] + ';', 'g'), entity[1]);
	});
	return text;
};

/**
 * Encodes HTML
 * @param text          To encode
 * @returns {string}    Encoded
 */
const encodeHTML = function (text) {
	console.log('encode input', text);
	HTMLEntities.forEach(entity => {
		text = text.replace(new RegExp(entity[1], 'g'), entity[0] + ';');
	});

	console.log('encode output', text);
	return encodeURIComponent(encodeURIComponent(text));
};

/**
 * Gets distance from bottom of the screen
 * @returns {number}
 */
const getDistFromBottom = function () {

	var scrollPosition = window.pageYOffset;
	var windowSize = window.innerHeight;
	var bodyHeight = document.body.offsetHeight;

	return Math.max(bodyHeight - (scrollPosition + windowSize), 0);

};

/**
 * Converts a template string into a HTML element
 * @param html          HTML string to be converted
 * @returns {Element}   HTML element
 */
const htmlToElement = function(html) {
	var template = document.createElement('template');
	template.innerHTML = html;
	return template.content.firstChild;
};