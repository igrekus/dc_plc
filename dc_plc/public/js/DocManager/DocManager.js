// import ToolRoot from './ToolRoot.vue';

frappe.provide('frappe.dc_plc');

frappe.dc_plc.DocManager = class {
	constructor({ parent }) {
		this.$parent = $(parent);
		this.page = parent.page;
		this.setup_header();
		this.make_body();
	}
	make_body() {
		$(frappe.render_template('<div id="app">LOL MANAGER HAHAHA</div>', this.page)).prependTo(this.$parent.find('.layout-main'));
	}

	setup_header() {
	}

	set_products_ids(ids) {
		this.vue.$children[0].product_ids = ids;
	}
};
