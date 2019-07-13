(function () {

	frappe.provide('frappe.dc_plc.utils');
	frappe.require('assets/dc_plc/js/utils/formatter.js', () => {
		frappe.dc_plc.utils.product_link_formatter = product_link_formatter;
		frappe.dc_plc.utils.function_link_formatter = function_link_formatter;
		frappe.dc_plc.utils.full_stat_formatter = full_stat_formatter;
	});

	console.log('>>> DC PLC init finished <<<');
})();
