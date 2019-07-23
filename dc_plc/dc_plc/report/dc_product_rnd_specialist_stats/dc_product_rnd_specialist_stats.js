// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DC Product RND Specialist Stats"] = {
	filters: [],
	formatter: frappe.dc_plc.utils.formatters.rnd_spec_formatter,
	after_datatable_render: table_instance => {
		let highlight_cols = [5];
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
