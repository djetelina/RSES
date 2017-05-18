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

 drawIngredientTable  (limit, offset) {
	fetch('/rses/api/list/ingredient_type/' + limit + '/' + offset, {credentials: "include"})
		.then(res => res.json())
		.then((out) => {

			let table_content = document.getElementById('ingredient-types-table');
			table_content.innerHTML = "";
			for (leti = 0; i < out.ingredient_types.length; i++) {
				this.insertIngredientTableRow(table_content, out.ingredient_types[i])
			}
		})
		.catch(err => console.error(err));
};

	insertIngredientTableRow (parent, ingredient_type) {
		let tableRow, rowName, rowActions, deleteButton, editButton;
		tableRow = document.createElement("tr");
		rowName = document.createElement("td");
		rowActions = document.createElement("td");
		rowActions.className = "text-center";

		deleteButton = createDeleteButton(
			{name: 'ingredient-type-id', id: ingredient_type.id},
			this.deleteIngredientType
		);

		editButton = createEditButton(
			{name: 'ingredient-type-id', id: ingredient_type.id},
			this.editIngredientType
		);

		rowActions.appendChild(editButton);
		rowActions.appendChild(deleteButton);
		tableRow.appendChild(rowName).innerHTML = ingredient_type.name;
		tableRow.appendChild(rowActions);
		tableRow.setAttribute('ingredient-type-id', ingredient_type.id);
		parent.appendChild(tableRow);
	};

	deleteIngredientType (event) {
		let targetIngredientTypeId = event.target.getAttribute('ingredient-type-id');
		fetch('/rses/api/ingredient_type/' + targetIngredientTypeId, {credentials: "include", method: 'delete'})
			.then(res => res.json())
			.then((out) => {})
			.catch(err => console.error(err));
	};

	editIngredientType (event) {
		let targetRow = event.target.parentNode.parentNode;
		let targetIngredientTypeId = event.target.getAttribute('ingredient-type-id');
		let modal = document.getElementById('edit-modal');
		let name = document.getElementById('edit-name');
		name.value = targetRow.childNodes[0].innerHTML;
		document.getElementById('edit-submit').addEventListener("click", function handler (event) {
			fetch('/rses/api/ingredient_type/' + targetIngredientTypeId + '/name/' + name.value,
				{credentials: "include", method: 'post'})
				.then(res => res.json())
				.then((out) => {
					notifySuccess("Ingredient Type edited, new name: '" + out.new_name + "'");
				})
				.catch(err => console.error(err));
			event.currentTarget.removeEventListener(event.type, handler)
		});
	}
}

let ingredient_types = new IngredientTypes();

window.addEventListener("click", function () {
	let ingredient_types = new IngredientTypes();
});