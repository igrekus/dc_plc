frappe.provide('dc_plc.export_app');

frappe.pages['dc_product_export'].on_page_load = function(wrapper) {
	// create page when loaded for the first time in the session
	this.page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Экспорт записей о продукции НО-8",
		single_column: true,
	});
};

frappe.pages['dc_product_export'].refresh = function(wrapper) {
	let product_ids = [];
	if (frappe.has_route_options()) {
		product_ids = frappe.route_options.export_products;
	} else {
		console.log('generating empty table');
	}

	show_product_export_page(this.page, product_ids);
};

show_product_export_page = (page, ids) => {
	let app_div = $('#export-app');
	if (!app_div.length) {
		$(frappe.render_template('dc_product_export', page)).prependTo(page.main);
		// TODO hook up Vue to rendered template
		frappe.dc_plc.export_app = new Vue({
			el: '#export-app',
			data: {
				product_ids: 'ids',
			}
		});
	}
};
