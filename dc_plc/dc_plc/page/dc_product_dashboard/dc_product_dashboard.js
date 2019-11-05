frappe.provide("dc_plc");

frappe.pages["dc_product_dashboard"].on_page_load = (wrapper) => {

	this.page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Статистика заполненности и актуальности",
		single_column: true,
		data: {
			role_stat: [],
			dev_stat: [],
		},
	});

	this.page.add_menu_item(__("Menu item 1"), () => {
		console.log("menu item 1");
	}, 'fa fa-th');

	let page = this.page;

	Promise.all([
		get_role_completeness_stats(),
		get_developer_completeness_stats(),
	]).then(r => {
		let [role_stat, dev_stat] = r;

		page.data.role_stat = role_stat.message;
		page.data.dev_stat = dev_stat.message;
 		page.data.dev_stat[0].url = `http://${window.location.host}/desk#query-report/DC%20Product%20Developer%20Stats/Report?developer=HR-EMP-00094`;

		render_dashboard(page);
	});
};

frappe.pages['dc_product_dashboard'].on_page_show = () => {
	frappe.breadcrumbs.add("DC PLC");
};

let get_role_completeness_stats = () => frappe.call({
	method: 'dc_plc.controllers.dashboard_query.role_completeness_stats',
}).promise();

let get_developer_completeness_stats = () => frappe.call({
	method: 'dc_plc.controllers.dashboard_query.developer_completeness_stats',
}).promise();

let render_dashboard = (page) => $(frappe.render_template("dc_product_dashboard", page)).prependTo(page.main);
