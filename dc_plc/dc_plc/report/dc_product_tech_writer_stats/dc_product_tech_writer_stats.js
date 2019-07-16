// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DC Product Tech Writer Stats"] = {
	filters: [],
	formatter: frappe.dc_plc.utils.formatters.tech_writer_formatter,
	onload: report => {
		let highlight_cols = [12, 13, 14];
		let sheet = window.document.styleSheets[0];
		highlight_cols.forEach((el) => {
			sheet.insertRule(`.dt-instance-1 .dt-cell--col-${el} { background-color: rgba(255, 252, 29, 0.27); }`, sheet.cssRules.length);
		});
	}
};
