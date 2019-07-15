(function () {

	frappe.provide('frappe.dc_plc.utils');
	frappe.require('assets/dc_plc/js/utils/formatter.js', () => {
		frappe.dc_plc.utils.product_link_formatter = product_link_formatter;
		frappe.dc_plc.utils.function_link_formatter = function_link_formatter;
		frappe.dc_plc.utils.full_stat_formatter = full_stat_formatter;
		frappe.dc_plc.utils.rnd_project_link_formatter = rnd_project_link_formatter;
		frappe.dc_plc.utils.product_type_link_formatter = product_type_link_formatter;
		frappe.dc_plc.utils.package_link_formatter = package_link_formatter;
	});

	console.log('>>> DC PLC init finished <<<');
})();
