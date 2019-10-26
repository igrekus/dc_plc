frappe.pages['doc_manager'].on_page_load = function(wrapper) {
	this.page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Менеджер документов',
		single_column: true,
	});

	// this.page.$export_tool = new frappe.dc_plc.ExportTool(this.page);
};

frappe.pages['doc_manager'].on_page_show = () => {
	frappe.breadcrumbs.add("DC PLC");
};
