frappe.listview_settings['DC_PLC_Product_Summary'] = {
	add_fields: ["display_type", "display_proj_title", "display_func", "display_package"],
	// filters:[["display_type","=", "Open"]],

	onload: function (view) {
		// frappe.set_route("List", "DC_PLC_Product_Summary/Report");
	},
	refresh: function(doc, dt, dn) {
		// frappe.set_route("List", "DC_PLC_Product_Summary/Report");
		console.log(">>> list refresh");
	}

};
