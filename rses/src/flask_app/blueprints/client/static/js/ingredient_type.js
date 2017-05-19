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

		const response = await fetchRsesCatch('/list/total/ingredient_type', 'get');
		document.getElementById('ingredient-type-total').innerHTML = response.total;
	};

    async drawIngredientTable  (offset) {
	    const limit = document.getElementById('limit-ingredient-type').value;
	    const nameFilter = document.getElementById('filter-ingredient-type').value;

	    let url = `/list/ingredient_type/${limit}/${offset}`;
	    if (nameFilter) {
	        url += `/${nameFilter}`
		}

		const tableContent = document.getElementById('ingredient-types-table');
	    tableContent.innerHTML = `<tr><td colspan="2" align="center"><i class="text-info fa fa-refresh fa-spin fa-2x fa-fw"></i>
									<span class="sr-only">Loading...</span></td></tr>`;

		const response = await fetchRsesCatch(url, 'get');
		tableContent.innerHTML= '';
		response.ingredient_types.forEach(item => {
			this.insertIngredientTableRow(tableContent, item)
		});
};

	insertIngredientTableRow (parent, ingredient_type) {
		const tableRow = document.createElement("tr");
		const rowName = document.createElement("td");
		const rowActions = document.createElement("td");
		rowActions.className = "text-center";

		const deleteButton = createDeleteButton(
			{name: 'ingredient-type-id', id: ingredient_type.id},
			this.deleteIngredientType
		);

		const editButton = createEditButton(
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
		const modal = document.getElementById('create-modal');
		const name = document.getElementById('create-name');
		fetchRses('/ingredient_type/new/' + name.value, 'post')
			.then(out => {
				notifySuccess(`Ingredient Type '${name.value}' created`);
				refreshIngredientTypes();
			})
			.catch(err => {
				notifyError(err);
			});
		name.value = "";
	};

	deleteIngredientType (event) {
		const targetIngredientTypeId = event.target.getAttribute('ingredient-type-id');
		const name = event.target.parentNode.parentNode.childNodes[0].innerHTML;
		fetchRses(`/ingredient_type/${targetIngredientTypeId}`, 'delete')
			.then(out => {
				notifySuccess(`Deleted '${name}'`);
				refreshIngredientTypes();
			})
			.catch(err => notifyError(err));
	};

	editIngredientType (event) {
		const targetRow = event.target.parentNode.parentNode;
		const targetIngredientTypeId = event.target.getAttribute('ingredient-type-id');
		const modal = document.getElementById('edit-modal');
		const name = document.getElementById('edit-name');
		name.value = targetRow.childNodes[0].innerHTML;
		const submitButtonOld = document.getElementById('edit-submit');
		const submitButton = submitButtonOld.cloneNode(true);
		submitButtonOld.parentNode.replaceChild(submitButton, submitButtonOld);
		submitButton.addEventListener("click", function handlerEdit () {
			fetchRses(`/ingredient_type/${targetIngredientTypeId}/name/${name.value}`,
				'post')
				.then((out) => {
					notifySuccess(`Ingredient Type edited, new name: '${out.new_name}'`);
					refreshIngredientTypes();
				})
				.catch(err => notifyError(err));
		});
	}
}


const refreshIngredientTypes = function () {
	let ingredient_types = new IngredientTypes();
};

refreshIngredientTypes();