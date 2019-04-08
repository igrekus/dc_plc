// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DC Product Stats"] = {
	// add filter to report table header
	"filters": [

	],
	get_datatable_options(options) {
		return {
			...options,
            inlineFilters: true,
            layout: 'fixed',
            dynamicRowHeight: false,
		}
	},
	after_datatable_render: function (datatable_obj) {
		let els = $(datatable_obj.wrapper).find(".dt-row");
		for (let i = 2; i < els.length; ++i) {
			els[i].style = {
				position: "",
				top: "",
			};
			els[i].style.cssText += "height: auto;";
		}
	},
	// onload(report) {
	// 	console.log("refresh");
	//
	// 	report.page.add_inner_button(__("Accounts Payable"), function () {
	// 		var filters = report.get_values();
	// 		frappe.set_route('query-report', 'Accounts Payable', {company: filters.company});
	// 	});
	// },
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
