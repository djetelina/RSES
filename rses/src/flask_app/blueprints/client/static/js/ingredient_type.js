/**
 * Created by David on 17.05.2017.
 */

class IngredientTypesClass {
	constructor () {
		this.loading = false;
		this.loaded = 0;
		this.allLoaded = false;
		this.tableContent = document.getElementById('ingredient-types-table');
		this.total = 0;
		this.getIngredientTypeTotal();
		this.drawIngredientTable();
	}

	async getIngredientTypeTotal () {
		document.getElementById('ingredient-type-total').innerHTML = `<i class="fa fa-refresh fa-spin fa-fw"></i>`;

		const response = await fetchRsesCatch('/list/total/ingredient_type', 'get');
		document.getElementById('ingredient-type-total').innerHTML = response.total;
		this.total = response.total;
	};

    async drawIngredientTable  (reload = true) {
    	this.loading = true;
	    const limit = 20;
	    const nameFilter = document.getElementById('filter-ingredient-type').value;
	    if (reload) this.loaded = 0;

	    let url = `/list/ingredient_type/${limit}/${this.loaded}`;
	    if (nameFilter) {
	        url += `/${nameFilter}`
		}

		let response;

	    if (this.loaded === 0) {
		    this.tableContent.innerHTML = tableLoading();
		    response = await fetchRsesCatch(url, 'get');
		    this.tableContent.innerHTML = '';
	    } else {
	    	this.tableContent.insertAdjacentHTML('beforeend', tableLoading());
		    response = await fetchRsesCatch(url, 'get');
		    this.tableContent.removeChild(this.tableContent.lastChild);
	    }

	    this.loaded += limit;

		response.ingredient_types.forEach(item => {
			this.insertIngredientTableRow(this.tableContent, item)
		});
		this.loading = false;
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
		rowName.innerHTML = ingredient_type.name;
		tableRow.appendChild(rowName);
		tableRow.appendChild(rowActions);
		tableRow.setAttribute('ingredient-type-id', ingredient_type.id);
		parent.appendChild(tableRow);
	};

	static async createIngredientType () {
		const modal = document.getElementById('create-modal');
		const name = document.getElementById('create-name');
		fetchRses(`/ingredient_type/new/${encodeHTML(name.value)}`, 'post')
			.then(out => {
				notifySuccess(`Ingredient Type '${name.value}' created`);
				refreshIngredientTypes();
			})
			.catch(err => {
				notifyError(err);
			})
			.then(out => name.value = "");
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
		console.debug(name.value);
		console.debug(decodeHTML(targetRow.childNodes[0].innerHTML));
		name.value = decodeHTML(targetRow.childNodes[0].innerHTML);
		console.debug(name.value);
		const submitButtonOld = document.getElementById('edit-submit');
		const submitButton = submitButtonOld.cloneNode(true);
		submitButtonOld.parentNode.replaceChild(submitButton, submitButtonOld);
		submitButton.addEventListener("click", function handlerEdit () {
			fetchRses(`/ingredient_type/${targetIngredientTypeId}/name/${encodeHTML(name.value)}`,
				'post')
				.then((out) => {
					notifySuccess(`Ingredient Type edited, new name: '${out.new_name}'`);
					refreshIngredientTypes();
				})
				.catch(err => notifyError(err));
		});
	}
}

document.addEventListener('scroll', function () {
	if (!ingredientTypes.loading &&
		getDistFromBottom() > 0 &&
		getDistFromBottom() <= 8888 &&
		ingredientTypes.loaded < ingredientTypes.total) {
		ingredientTypes.drawIngredientTable(false);
	} else if (ingredientTypes.loaded >= ingredientTypes.total && !ingredientTypes.allLoaded) {
		ingredientTypes.allLoaded = true;
		ingredientTypes.tableContent.insertAdjacentHTML('beforeend',
			`<tr><td colspan="2" align="center">Nothing more to load.</td></tr>`
		)

	}
});

$('#edit-modal').on('shown.bs.modal', function () {
	$('#edit-name').focus()
});

$('#create-modal').on('shown.bs.modal', function () {
	$('#create-name').focus()
});

const refreshIngredientTypes = function () {
	ingredientTypes.allLoaded = false;
	ingredientTypes.total = ingredientTypes.getIngredientTypeTotal();
	ingredientTypes.drawIngredientTable();
};

let ingredientTypes = new IngredientTypesClass();