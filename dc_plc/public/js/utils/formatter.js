let full_stat_formatter = (value, row, column, row_data, format) => {
	if (!value) {
		value = '-';
	}
	if (column.colIndex === 3) {   // Relevance column
		value = parseInt(value.split('|')[0]).toString() + '%';
	}
	if (column.colIndex === 4) {   // Progress column
		value = value.toString() + '%';
	}
	return `<a href="http://${window.location.host}/desk#Form/DC_PLC_Product_Summary/${row_data.ID}">${value}</a>`;
};


// Role query formatters
let template_role_formatter = (handler, value, row, column, row_data, format) => {
	if (!value) {
		value = '-';
	}
	if (column.colIndex === 2) {   // Relevance column
		let id = row_data.ID;
		let [date, check, perms] = value.split(';');
		let check_str = parseInt(check) ? 'checked' : '';
		if (parseInt(perms)) {
			return `<input type="checkbox" data-index="${row.meta.rowIndex}" id="${id}" onchange="${handler}(this)" ${check_str}/><label style="vertical-align: top; padding-top: 3px;" class="rel_label_${id}" for="${id}">&nbsp&nbsp${date}</label>`
		}
		value = date;
	}
	return `<a href="http://${window.location.host}/desk#Form/DC_PLC_Product_Summary/${row_data.ID}">${value}</a>`;
};

let mmic_dept_head_formatter = (...args) => {
	return template_role_formatter('frappe.dc_plc.utils.handlers.mmic_dept_head_handler', ...args);
};

let rnd_spec_formatter = (...args) => {
	return template_role_formatter('frappe.dc_plc.utils.handlers.rnd_spec_handler', ...args);
};

let developer_formatter = (...args) => {
	return template_role_formatter('frappe.dc_plc.utils.handlers.developer_handler', ...args);
};

let opcon_spec_formatter = (...args) => {
	return template_role_formatter('frappe.dc_plc.utils.handlers.opcon_spec_handler', ...args);
};

let procmap_spec_formatter = (...args) => {
	return template_role_formatter('frappe.dc_plc.utils.handlers.procmap_spec_handler', ...args);
};

let desdoc_spec_formatter = (...args) => {
	return template_role_formatter('frappe.dc_plc.utils.handlers.desdoc_spec_handler', ...args);
};

let tech_writer_formatter = (...args) => {
	return template_role_formatter('frappe.dc_plc.utils.handlers.tech_writer_handler(this)', ...args);
};


// Filter query formatters
let template_link_formatter = (filter, title_col, value, row, column, row_data, format) => {
	if (!value) {
		value = '-';
	}
	let [title, id] = row[title_col].content.split('|');
	if (column.colIndex === title_col) {   // Title column
		value = title;
	}
	return `<a href="http://${window.location.host}/desk#query-report/DC%20Product%20Stats/Report?${filter}=${id}">${value}</a>`;
};

let function_link_formatter = (...args) => {
	return template_link_formatter('link_function', 2, ...args);
};

let rnd_project_link_formatter = (...args) => {
	return template_link_formatter('link_rnd_project', 1, ...args);
};

let product_type_link_formatter = (...args) => {
	return template_link_formatter('link_type', 1, ...args);
};

let package_link_formatter = (...args) => {
	return template_link_formatter('link_package', 1, ...args);
};

let letter_link_formatter = (...args) => {
	return template_link_formatter('link_letter', 1, ...args);
};

let status_link_formatter = (...args) => {
	return template_link_formatter('link_status', 1, ...args);
};
