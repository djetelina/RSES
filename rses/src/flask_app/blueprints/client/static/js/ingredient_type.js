/**
 * Created by David on 17.05.2017.
 */

class IngredientTypes {
	constructor () {
		this.getIngredientTypeTotal();
		this.drawIngredientTable(50, 0);
	}

	getIngredientTypeTotal () {
		fetch('/rses/api/list/total/ingredient_type', {credentials: "include"})
			.then(res => res.json())
			.then((out) => {
				console.debug('getIngredientTypeTotal response');
				console.debug(out);
				document.getElementById('ingredient-type-total').innerHTML = out.total;
			})
			.catch(err => console.error(err));
	};

	drawIngredientTable (limit, offset) {
		fetch('/rses/api/list/ingredient_type/' + limit + '/' + offset, {credentials: "include"})
			.then(res => res.json())
			.then((out) => {
				console.debug(out.ingredient_types);
				let table_content = document.getElementById('ingredient-types-table');
				table_content.innerHTML = "";
				for (let i = 0; i < out.ingredient_types.length; i++) {
					this.insertIngredientTableRow(table_content, out.ingredient_types[i])
				}
			})
			.catch(err => console.error(err));
	};

	insertIngredientTableRow (parent, ingredient_type) {
		let table_row, row_name, row_actions, delete_button;
		table_row = document.createElement("tr");
		row_name = document.createElement("td");
		row_actions = document.createElement("td");
		row_actions.className = "text-center"
		// TODO create elsewhere
		delete_button = document.createElement("i");
		delete_button.className = "fa fa-trash-o text-danger";
		delete_button.setAttribute('ingredient-type-id', ingredient_type.id);
		delete_button.setAttribute('aria-hidden', 'true');
		delete_button.addEventListener("click", this.deleteIngredientType);
		row_actions.appendChild(delete_button);
		table_row.appendChild(row_name).innerHTML = ingredient_type.name;
		table_row.appendChild(row_actions);
		table_row.setAttribute('ingredient-type-id', ingredient_type.id);
		parent.appendChild(table_row);
	};

	deleteIngredientType (element) {
		// TODO
		console.log("click");
	};
}

let ingredient_types = new IngredientTypes();

window.addEventListener("click", function () {
	let ingredient_types = new IngredientTypes();
});