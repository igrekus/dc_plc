// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DC Product Tech Writer Stats"] = {
	filters: [],
	formatter: frappe.dc_plc.utils.formatters.tech_writer_formatter,
	after_datatable_render: table_instance => {
		let highlight_cols = [12, 13, 14];
		highlight_cols.forEach(col => {
			table_instance.style.setStyle(`.dt-cell--col-${col}`, {backgroundColor: 'rgba(255, 252, 29, 0.27);'})
		});
	},
	onload: report => {
		report.export_products = [];
		report.page.set_title_sub('');
		report.page.clear_actions_menu();
	}
};
