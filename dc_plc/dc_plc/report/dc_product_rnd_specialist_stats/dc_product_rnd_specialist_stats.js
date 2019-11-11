// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DC Product RND Specialist Stats"] = {
	filters: [],
	formatter: frappe.dc_plc.utils.formatters.rnd_spec_formatter,
	after_datatable_render: table_instance => {
		let highlight_cols = [5];
		let data = table_instance.datamanager.data;

		for (let row = 0; row < data.length; ++row) {
			const [date, check, perms] = data[row][__('Relevance')].split(';');
			const is_checked = !!parseInt(check);
			highlight_cols.forEach(col => {
				let bgCol = is_checked ? 'rgba(37,220,2,0.2);' : 'rgba(255, 252, 29, 0.27);';
				table_instance.style.setStyle(`.dt-cell--${col}-${row}`, {backgroundColor: `${bgCol}`});
			});
		}
		table_instance.style.setStyle(`.dt-scrollable`, {height: '550px;'});
	},
	onload: report => {
		report.export_products = [];
		report.page.set_title_sub('');
		report.page.clear_actions_menu();
	}
};
