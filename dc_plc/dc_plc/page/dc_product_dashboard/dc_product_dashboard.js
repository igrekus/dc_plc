frappe.provide("dc_plc");

frappe.pages["dc_product_dashboard"].on_page_load = (wrapper) => {

	this.page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Product dashboard",
		single_column: true,
		role_completeness: []
	});

	frappe.dc_plc.show_dashboard(this.page);

	// me.page.main.on("click", ".activity-message", function() {
	// 	var link_doctype = $(this).attr("data-link-doctype"),
	// 		link_name = $(this).attr("data-link-name"),
	// 		doctype = $(this).attr("data-doctype"),
	// 		docname = $(this).attr("data-docname");
	//
	// 	if (doctype && docname) {
	// 		if (link_doctype && link_name) {
	// 			frappe.route_options = {
	// 				scroll_to: { "doctype": doctype, "name": docname }
	// 			}
	// 		}
	//
	// 		frappe.set_route(["Form", link_doctype || doctype, link_name || docname]);
	// 	}
	// });

	// Build Report Button
	this.page.add_menu_item(__("Menu item 1"), () => {
		console.log("menu item 1");
		// frappe.route_options = {
		// 	"user": frappe.session.user
		// };
		// frappe.set_route("List", "Feed", "Report");
	}, 'fa fa-th');
	// this.page.add_button("BOTON", () => console.log("BOTON"), "fa fa-th", false);
	// this.page.add_inner_button("BOTON", () => console.log("BOTON"), "test", type="default");
};

frappe.pages['dc_product_dashboard'].on_page_show = () => {
	frappe.breadcrumbs.add("DC PLC");
};

get_role_completeness_stats = (page) => {
	frappe.call({
		method: "dc_plc.controllers.queries.role_completeness_stats",
		callback: (r) => {
			if (r.message) {
				page.role_completeness = r.message;
				frappe.dc_plc.render_dashboard(page);
			}
		}
	});
};

frappe.dc_plc.show_dashboard = (page) => {
	get_role_completeness_stats(page);
};

frappe.dc_plc.render_dashboard = (page) => {
	page.title = __("Product info completeness statistics");
	$(frappe.render_template("dc_product_dashboard", page)).prependTo(page.main);
};
