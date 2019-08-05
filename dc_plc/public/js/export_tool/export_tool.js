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
		$(frappe.render_template('<div id="app"><tool-root></tool-root></div>', this.page)).prependTo(this.$parent.find('.layout-main'));
		this.vue = new Vue({
			el: '#app',
			data: function () {
				return {}
			},
			components: {
				ToolRoot
			}
		});
	}

	setup_header() {
	}

	set_products_ids(ids) {
		this.vue.$children[0].product_ids = ids;
	}
};
