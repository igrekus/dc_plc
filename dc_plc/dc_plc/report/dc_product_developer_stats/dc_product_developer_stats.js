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
		let data = table_instance.datamanager.data;
		for (let row = 0; row < data.length; ++row) {
			const [date, check, perms] = data[row][__('Relevance')].split(';');
			const is_checked = !!parseInt(check);
			highlight_cols.forEach(col => {
				let bgCol = is_checked ? 'rgba(37,220,2,0.2);' : 'rgba(255, 252, 29, 0.27);';
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: `${bgCol}`});
			});
		}
	},
	onload: report => {
		report.export_products = [];
		report.page.set_title_sub('');
		report.page.clear_actions_menu();
	}
};
