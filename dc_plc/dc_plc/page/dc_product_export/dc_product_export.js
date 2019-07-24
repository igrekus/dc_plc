frappe.pages['dc_product_export'].on_page_load = function(wrapper) {
	// create page when loaded for the first time in the session
	this.page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Экспорт записей о продукции НО-8",
		single_column: true,
	});

	this.page.$export_tool = new frappe.dc_plc.ExportTool(this.page);
};

frappe.pages['dc_product_export'].refresh = function(wrapper) {
	let product_ids = ["PROD000001", "PROD000014"];

	if (frappe.has_route_options()) {
		product_ids = frappe.route_options.export_products;
	} else {
		console.log('generating empty table');
	}

	this.page.$export_tool.set_products_ids(product_ids);
};
