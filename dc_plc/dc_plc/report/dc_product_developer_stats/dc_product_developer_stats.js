// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

let check_handle = (o) => {
	let relevant = o.checked;
	let name = o.id;
	frappe.call({
		method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary.set_developer_relevant",
		args: {
			name: name,
			relevant: relevant ? 1 : 0,
		},
		callback: r => {
			let { date, check } = r.message;
			$('.rel_label_' + name)[0].innerHTML = "&nbsp;&nbsp;" + date;
			o.checked = !!check;
		}
	});
};

frappe.query_reports["DC Product Developer Stats"] = {
	"filters": [

	],
	formatter: frappe.dc_plc.utils.product_link_formatter,
};
