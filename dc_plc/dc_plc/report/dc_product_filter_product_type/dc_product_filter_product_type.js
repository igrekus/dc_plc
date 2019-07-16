// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DC Product Filter Product Type"] = {
	"filters": [
	],
	formatter: frappe.dc_plc.utils.formatters.product_type_link_formatter,
};
