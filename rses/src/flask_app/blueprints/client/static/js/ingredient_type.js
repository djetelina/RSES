/**
 * Created by David on 17.05.2017.
 */

class IngredientTypes {
	constructor () {
		this.getIngredientTypeTotal();
		this.drawIngredientTable(0);
	}

	async getIngredientTypeTotal () {
		document.getElementById('ingredient-type-total').innerHTML = `<i class="fa fa-refresh fa-spin fa-fw"></i>`;

		let response = await fetchRses('/list/total/ingredient_type', 'get');
		document.getElementById('ingredient-type-total').innerHTML = response.total;
	};

    async drawIngredientTable  (offset) {
	    let limit = document.getElementById('limit-ingredient-type').value;
	    let nameFilter = document.getElementById('filter-ingredient-type').value;

	    let url = '/list/ingredient_type/' + limit + '/' + offset;
	    if (nameFilter) {
	        url += '/' + nameFilter
		}

		let tableContent = document.getElementById('ingredient-types-table');
	    tableContent.innerHTML = `<tr><td colspan="2" align="center"><i class="text-info fa fa-refresh fa-spin fa-2x fa-fw"></i>
									<span class="sr-only">Loading...</span></td></tr>`;

		let response = await fetchRses(url, 'get');
		tableContent.innerHTML= '';
		response.ingredient_types.forEach(item => {
			this.insertIngredientTableRow(tableContent, item)
		});
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

	static async createIngredientType () {
		let modal = document.getElementById('create-modal');
		let name = document.getElementById('create-name');
		await fetchRses('/ingredient_type/new/' + name.value, 'post');
		notifySuccess("Ingredient Type '" + name.value + "' created");
		refreshIngredientTypes();
		name.value = "";
	};

	deleteIngredientType (event) {
		let targetIngredientTypeId = event.target.getAttribute('ingredient-type-id');
		let name = event.target.parentNode.parentNode.childNodes[0].innerHTML;
		fetch('/rses/api/ingredient_type/' + targetIngredientTypeId, {credentials: "include", method: 'delete'})
			.then(res => res.json())
			.then((out) => {
				notifySuccess("Deleted '" + name + "'");
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
		let submitButtonOld = document.getElementById('edit-submit');
		let submitButton = submitButtonOld.cloneNode(true);
		submitButtonOld.parentNode.replaceChild(submitButton, submitButtonOld);
		submitButton.addEventListener("click", function handlerEdit () {
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