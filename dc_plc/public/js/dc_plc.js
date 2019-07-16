(function () {

	frappe.provide('frappe.dc_plc.utils');
	frappe.provide('frappe.dc_plc.utils.handlers');
	frappe.provide('frappe.dc_plc.utils.formatters');

	frappe.require('assets/dc_plc/js/utils/formatter.js', () => {
		frappe.dc_plc.utils.formatters.mmic_dept_head_formatter = mmic_dept_head_formatter;
		frappe.dc_plc.utils.formatters.rnd_spec_formatter = rnd_spec_formatter;
		frappe.dc_plc.utils.formatters.developer_formatter = developer_formatter;
		frappe.dc_plc.utils.formatters.opcon_spec_formatter = opcon_spec_formatter;
		frappe.dc_plc.utils.formatters.procmap_spec_formatter = procmap_spec_formatter;
		frappe.dc_plc.utils.formatters.desdoc_spec_formatter = desdoc_spec_formatter;
		frappe.dc_plc.utils.formatters.tech_writer_formatter = tech_writer_formatter;

		frappe.dc_plc.utils.formatters.full_stat_formatter = full_stat_formatter;

		frappe.dc_plc.utils.formatters.function_link_formatter = function_link_formatter;
		frappe.dc_plc.utils.formatters.rnd_project_link_formatter = rnd_project_link_formatter;
		frappe.dc_plc.utils.formatters.product_type_link_formatter = product_type_link_formatter;
		frappe.dc_plc.utils.formatters.package_link_formatter = package_link_formatter;
		frappe.dc_plc.utils.formatters.letter_link_formatter = letter_link_formatter;
		frappe.dc_plc.utils.formatters.status_link_formatter = status_link_formatter;
	});

	frappe.require('assets/dc_plc/js/utils/handler.js', () => {
		frappe.dc_plc.utils.handlers.mmic_dept_head_handler = mmic_dept_head_handler;
		frappe.dc_plc.utils.handlers.rnd_spec_handler = rnd_spec_handler;
		frappe.dc_plc.utils.handlers.developer_handler = developer_handler;
		frappe.dc_plc.utils.handlers.opcon_spec_handler = opcon_spec_handler;
		frappe.dc_plc.utils.handlers.procmap_spec_handler = procmap_spec_handler;
		frappe.dc_plc.utils.handlers.desdoc_spec_handler = desdoc_spec_handler;
		frappe.dc_plc.utils.handlers.tech_writer_handler = tech_writer_handler;
	});

	console.log('>>> DC PLC init finished <<<');
})();
