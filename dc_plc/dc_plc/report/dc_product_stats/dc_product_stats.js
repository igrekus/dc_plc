// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.provide("frappe.dc_plc");

frappe.query_reports["DC Product Stats"] = {
	"filters": [
		{
			"label": __("RND Project"),
			"fieldname": "link_rnd_project",
			"fieldtype": "Link",
			"options": "DC_PLC_RND_Project"
		},
		{
			"label": __("Type"),
			"fieldname": "link_type",
			"fieldtype": "Link",
			"options": "DC_PLC_Product_Type"
		},
		{
			"label": __("Function"),
			"fieldname": "link_function",
			"fieldtype": "Link",
			"options": "DC_PLC_Product_Function"
		},
		{
			"label": __("Package"),
			"fieldname": "link_package",
			"fieldtype": "Link",
			"options": "DC_PLC_Package"
		},
		{
			"label": __("Status"),
			"fieldname": "link_status",
			"fieldtype": "Link",
			"options": "DC_PLC_Product_Status"
		},
		{
			"label": __("Letter"),
			"fieldname": "link_letter",
			"fieldtype": "Link",
			"options": "DC_PLC_Product_Letter"
		},
		{
			label: __("Developer"),
			fieldname: "developer",
			fieldtype: "Link",
			options: "Employee",
			get_query: (doc, cut, cdn) => {
				return {
					query: 'dc_plc.controllers.queries.developer_query_with_empty_developer'
				}
			}
		},
	],
	formatter: frappe.dc_plc.utils.formatters.full_stat_formatter,
	after_datatable_render: table_instance => {
		let data = table_instance.datamanager.data;
		for (let row = 0; row < data.length; ++row) {
			let array_str = data[row][__('Relevance')].split('|')[1];
			let index_str = array_str.slice(1, array_str.length - 1);
			if (index_str) {
				// TODO remove old styles
				let columns_to_highlight = index_str.split(', ').map(el => {
					return parseInt(el);
				});
				columns_to_highlight.forEach(col => {
					table_instance.style.setStyle(`.dt-cell--${col + 1}-${row}`, {backgroundColor: 'rgba(37,220,2,0.2);'});
				});
			}
		}
		table_instance.style.setStyle(`.dt-scrollable`, {height: '550px;'});
	},
	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
			events: {
				onCheckRow: function (data) {
					// this = current datatable instance
					let checked_rows = this.rowmanager.getCheckedRows();
					if (checked_rows.length) {
						frappe.query_report.page.show_actions_menu();
					} else {
						frappe.query_report.page.hide_actions_menu();
					}
				},
			}
		});
	},
	onload: report => {
		report.export_products = [];
		report.page.set_title_sub('');
		report.page.clear_actions_menu();
		// TODO HACK modify inner menu
		// remove inner toolbar with the "Set Chart" button
		$('.form-inner-toolbar').remove();
		// report.page.add_inner_button(__("Accounts Payable"), function () {
		// 	var filters = report.get_values();
		// 	frappe.set_route('query-report', 'Accounts Payable', {company: filters.company});
		// });
		// report.page.remove_inner_button('Set Chart');

		// TODO HACK modify main menu
		report.page.hide_menu();

		report.page.add_action_item('Add selected to export', () => {
			let new_rows = report.datatable.rowmanager.getCheckedRows().map(row => parseInt(row));
			new_rows.forEach(row => {
				let prod_id = report.data[row]['ID'];
				if (report.export_products.indexOf(prod_id) === -1) {
					report.export_products.push(prod_id);
				}
			});
			if (report.export_products.length) {
				report.page.set_title_sub(`Export ${report.export_products.length} products`);
				console.log('exporting:', report.export_products);
			}
		}, true);

		report.page.add_action_item(`Export added products`, () => {
			if (report.export_products.length) {
				frappe.set_route("dc_product_export", "", {export_products: report.export_products});
			}
		}, true);

		report.page.hide_actions_menu();
	},

	// get_chart_data: function (columns, result) {
	// 	return {
	// 		data: {
	// 			labels: result.map(d => d[0]),
	// 			datasets: [{
	// 				name: 'Mins to first response',
	// 				values: result.map(d => d[1])
	// 			}]
	// 		},
	// 		type: 'line',
	// 	}
	// }
};
