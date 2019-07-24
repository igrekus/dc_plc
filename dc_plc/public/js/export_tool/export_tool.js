import ToolRoot from './ToolRoot.vue';

frappe.provide('frappe.dc_plc');

frappe.dc_plc.ExportTool = class {
	constructor({ parent }) {
		this.$parent = $(parent);
		this.page = parent.page;
		this.setup_header();
		this.make_body();
	}
	make_body() {
		this.$export_tool_container = this.$parent.find('.layout-main');
		this.vue = new Vue({
			el: this.$export_tool_container[0],
			data: {
			},
			render: h => h(ToolRoot),
		});
	}
	setup_header() {

	}

	set_products_ids(ids) {
		this.vue.$children[0].product_ids = ids;
	}
};
