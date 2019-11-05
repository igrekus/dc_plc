frappe.provide("dc_plc");

frappe.pages["dc_product_dashboard"].on_page_load = (wrapper) => {

	this.page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Статистика заполненности и актуальности",
		single_column: true,
		role_completeness: [],
		developer_completeness: []
	});

	frappe.dc_plc.show_dashboard(this.page);

	this.page.add_menu_item(__("Menu item 1"), () => {
		console.log("menu item 1");
	}, 'fa fa-th');
};

frappe.pages['dc_product_dashboard'].on_page_show = () => {
	frappe.breadcrumbs.add("DC PLC");
};

// TODO refactor callback hell
get_role_completeness_stats = (page) => {
	frappe.call({
		method: "dc_plc.controllers.dashboard_query.role_completeness_stats",
		callback: (r) => {
			if (r.message) {
				page.role_completeness = r.message;
				get_developer_completeness_stats(page);
			}
		}
	});
};

get_developer_completeness_stats = (page) => {
	frappe.call({
		method: "dc_plc.controllers.dashboard_query.developer_completeness_stats",
		callback: (r) => {
			if (r.message) {
				page.developer_completeness = r.message;
				page.developer_completeness[0].url = `http://${window.location.host}/desk#query-report/DC%20Product%20Stats/Report?developer=HR-EMP-00094`;
				frappe.dc_plc.render_dashboard(page);
			}
		}
	});
};

frappe.dc_plc.show_dashboard = (page) => {
	get_role_completeness_stats(page);
};

frappe.dc_plc.render_dashboard = (page) => {
	page.title = "";
	$(frappe.render_template("dc_product_dashboard", page)).prependTo(page.main);
};
