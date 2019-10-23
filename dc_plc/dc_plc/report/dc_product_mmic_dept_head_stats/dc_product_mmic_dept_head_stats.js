// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DC Product MMIC Dept Head Stats"] = {
	filters: [],
	formatter: frappe.dc_plc.utils.formatters.mmic_dept_head_formatter,
	after_datatable_render: table_instance => {
		let highlight_cols = [4, 6, 7];
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
	// get_datatable_options(options) {
	// 	return Object.assign(options, {
	// 		checkboxColumn: true,
	// 		events: {
	// 			onCheckRow: function (data) {
	// 				row_name = data[2].content;
	// 				row_values = data.slice(7).map(function (column) {
	// 					return column.content;
	// 				})
	// 				entry = {
	// 					'name': row_name,
	// 					'values': row_values
	// 				}
	//
	// 				let raw_data = frappe.query_report.chart.data;
	// 				let new_datasets = raw_data.datasets;
	//
	// 				var found = false;
	//
	// 				for (var i = 0; i < new_datasets.length; i++) {
	// 					if (new_datasets[i].name == row_name) {
	// 						found = true;
	// 						new_datasets.splice(i, 1);
	// 						break;
	// 					}
	// 				}
	//
	// 				if (!found) {
	// 					new_datasets.push(entry);
	// 				}
	//
	// 				let new_data = {
	// 					labels: raw_data.labels,
	// 					datasets: new_datasets
	// 				}
	//
	// 				setTimeout(() => {
	// 					frappe.query_report.chart.update(new_data)
	// 				}, 500)
	//
	//
	// 				setTimeout(() => {
	// 					frappe.query_report.chart.draw(true);
	// 				}, 1000)
	//
	// 				frappe.query_report.raw_chart_data = new_data;
	// 			},
	// 		}
	// 	});
	// }

};
