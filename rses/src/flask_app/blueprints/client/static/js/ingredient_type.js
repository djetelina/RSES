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
 	let name_filter = document.getElementById('filter-ingredient-type').value;
 	let url = '/rses/api/list/ingredient_type/' + limit + '/' + offset;
 	if (name_filter) {
 		url += '/' + name_filter
	}
	let table_content = document.getElementById('ingredient-types-table');
 	table_content.innerHTML = `<tr><td colspan="2" align="center"><i class="text-info fa fa-refresh fa-spin fa-2x fa-fw"></i>
								<span class="sr-only">Loading...</span></td></tr>`;
	fetch(url,
		{credentials: "include"})
		.then(res => res.json())
		.then((out) => {
		table_content.innerHTML= '';
			for (let i = 0; i < out.ingredient_types.length; i++) {
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

	static createIngredientType () {
		let modal = document.getElementById('create-modal');
		let name = document.getElementById('create-name');
		fetch('/rses/api/ingredient_type/new/' + name.value,
			{credentials: 'include', method: 'post'})
			.then(res => res.json())
			.then((out) => {
				notifySuccess("Ingredient Type '" + name.value + "' created");
				refreshIngredientTypes();
				name.value = "";
			})
			.catch(err => console.error(err));
	};

	deleteIngredientType (event) {
		let targetIngredientTypeId = event.target.getAttribute('ingredient-type-id');
		let name = event.target.parentNode.parentNode.childNodes[0].innerHTML;
		fetch('/rses/api/ingredient_type/' + targetIngredientTypeId, {credentials: "include", method: 'delete'})
			.then(res => res.json())
			.then((out) => {
				notifySuccess("Deleted '" + name + "'")
				refreshIngredientTypes();
			})
			.catch(err => console.error(err));
	};

	editIngredientType (event) {
		let targetRow = event.target.parentNode.parentNode;
		let targetIngredientTypeId = event.target.getAttribute('ingredient-type-id');
		let modal = document.getElementById('edit-modal');
		let name = document.getElementById('edit-name');
		name.value = targetRow.childNodes[0].innerHTML;
		let submit_button_old = document.getElementById('edit-submit');
		let submit_button = submit_button_old.cloneNode(true);
		submit_button_old.parentNode.replaceChild(submit_button, submit_button_old);
		submit_button.addEventListener("click", function handlerEdit (event) {
			fetch('/rses/api/ingredient_type/' + targetIngredientTypeId + '/name/' + name.value,
				{credentials: "include", method: 'post'})
				.then(res => res.json())
				.then((out) => {
					notifySuccess("Ingredient Type edited, new name: '" + out.new_name + "'");
					refreshIngredientTypes();
				})
				.catch(err => console.error(err));
		});
	}
}


let refreshIngredientTypes = function () {
	let ingredient_types = new IngredientTypes();
};

refreshIngredientTypes();