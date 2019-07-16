// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DC Product MMIC Dept Head Stats"] = {
	filters: [],
	formatter: frappe.dc_plc.utils.formatters.mmic_dept_head_formatter,
	onload: report => {
		let highlight_cols = [4, 6, 7];
		let sheet = window.document.styleSheets[0];
		highlight_cols.forEach((el) => {
			sheet.insertRule(`.dt-instance-1 .dt-cell--col-${el} { background-color: rgba(255, 252, 29, 0.27); }`, sheet.cssRules.length);
		});
	}
};
