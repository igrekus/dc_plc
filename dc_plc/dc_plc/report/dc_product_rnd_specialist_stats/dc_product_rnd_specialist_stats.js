// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

let check_handle = (o) => {
	let relevant = o.checked;
	let name = o.id;
	frappe.call({
		method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary.set_rnd_spec_relevant",
		args: {
			name: name,
			relevant: relevant ? 1 : 0,
		},
		callback: r => {
			$('.rel_label_' + name)[0].innerHTML = "&nbsp;&nbsp;" + r.message;
		}
	});
};

frappe.query_reports["DC Product RND Specialist Stats"] = {
	"filters": [

	]
}
