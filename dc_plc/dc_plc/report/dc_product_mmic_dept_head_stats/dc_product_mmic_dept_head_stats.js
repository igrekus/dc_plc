// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

// TODO DRY this crap from all queries
let check_handle = (o) => {
	let relevant = o.checked;
	let name = o.id;
	frappe.call({
		method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary.set_dept_head_relevant",
		args: {
			name: name,
			relevant: relevant ? 1 : 0,
		},
		callback: r => {
			let {date, check} = r.message;
			$('.rel_label_' + name)[0].innerHTML = "&nbsp;&nbsp;" + date;
			o.checked = !!check;
		}
	});
};

frappe.query_reports["DC Product MMIC Dept Head Stats"] = {
	filters: [],
	formatter: frappe.dc_plc.utils.product_link_formatter,
	onload: report => {
		let highlight_cols = [4, 6, 7];
		let sheet = window.document.styleSheets[0];
		highlight_cols.forEach((el) => {
			sheet.insertRule(`.dt-instance-1 .dt-cell--col-${el} { background-color: rgba(255, 252, 29, 0.27); }`, sheet.cssRules.length);
		});
	}
};
