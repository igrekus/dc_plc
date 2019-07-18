// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DC Product Developer Stats"] = {
	"filters": [
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
	formatter: frappe.dc_plc.utils.formatters.developer_formatter,
	after_datatable_render: table_instance => {
		let highlight_cols = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16];
		highlight_cols.forEach(col => {
			table_instance.style.setStyle(`.dt-cell--col-${col}`, {backgroundColor: 'rgba(255, 252, 29, 0.27);'})
		});
	},

};
