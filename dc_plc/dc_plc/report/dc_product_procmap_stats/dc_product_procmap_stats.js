// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DC Product Procmap Stats"] = {
	filters: [],
	formatter: frappe.dc_plc.utils.formatters.procmap_spec_formatter,
	after_datatable_render: table_instance => {
		let highlight_cols = [7];
		highlight_cols.forEach(col => {
			table_instance.style.setStyle(`.dt-cell--col-${col}`, {backgroundColor: 'rgba(255, 252, 29, 0.27);'})
		});
	},
};
