frappe.listview_settings['dc_plc_product_summary'] = {
	add_fields: ["name", "ext_num", "asm_board"],
	//filters:[["status","=", "Open"]],
	// get_indicator: function(doc) {
	// 	if(doc.status=="Open" && doc.percent_complete) {
	// 		return [__("{0}% Complete", [cint(doc.percent_complete)]), "orange", "percent_complete,>,0|status,=,Open"];
	// 	} else {
	// 		return [__(doc.status), frappe.utils.guess_colour(doc.status), "status,=," + doc.status];
	// 	}
	// }
};
