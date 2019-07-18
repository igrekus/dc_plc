// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DC Product MMIC Dept Head Stats"] = {
	filters: [],
	formatter: frappe.dc_plc.utils.formatters.mmic_dept_head_formatter,
	// onload: report => {
	// 	// console.log('table onload');
	// },
	after_datatable_render: table_instance => {
		// $(table_instance.wrapper).find(".dt-row-0").find('input[type=checkbox]').click();
		let highlight_cols = [4, 6, 7];
		highlight_cols.forEach(col => {
			table_instance.style.setStyle(`.dt-cell--col-${col}`, { backgroundColor: 'rgba(255, 252, 29, 0.27);' })
		});
	},
};
