/**
 * Created by David on 17.05.2017.
 */

window.onload = function () {
	console.log('ingredient_type.js loaded');
	getIngredientTypeTotal();
	drawIngredientTable(50, 0);
};


let getIngredientTypeTotal = function () {
	fetch('/rses/api/list/total/ingredient_type', {credentials: "include"})
		.then(res => res.json())
		.then((out) => {
			console.debug('getIngredientTypeTotal response');
			console.debug(out);
			document.getElementById('ingredient-type-total').innerHTML += out.total;
		})
		.catch(err => console.error(err));
};

let insertIngredientTableRow = function (parent, ingredient_type) {
	table_row = document.createElement("tr");
	row_name = document.createElement("td");
	row_actions = document.createElement("td");
	// TODO create it elsewhere
	delete_button = document.createElement("button");
	delete_button.className = "btn btn-block btn-danger";
	delete_button.innerHTML = "DELETE";
	delete_button.setAttribute('onclick', 'deleteIngredientType(this)');
	row_actions.appendChild(delete_button);
	let row = parent.appendChild(table_row);
	row.appendChild(row_name).innerHTML = ingredient_type.name;
	row.appendChild(row_actions);
	row.setAttribute('ingredient-type-id', ingredient_type.id);
};

let drawIngredientTable = function (limit, offset) {
	fetch('/rses/api/list/ingredient_type/' + limit + '/' + offset, {credentials: "include"})
		.then(res => res.json())
		.then((out) => {
			console.debug(out.ingredient_types);
			let table_content = document.getElementById('ingredient-types-table');
			table_content.innerHTML = "";
			for (i = 0; i < out.ingredient_types.length; i++) {
				insertIngredientTableRow(table_content, out.ingredient_types[i])
			}
		})
		.catch(err => console.error(err));
};

let deleteIngredientType = function (element) {
	// TODO
	console.log("click");
};