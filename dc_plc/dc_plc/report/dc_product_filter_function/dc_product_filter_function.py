# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data()
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "function_group",
			"label": _("Function group"),
			"width": "150",
		},
		{
			"fieldname": "title",
			"label": _("Title"),
			"width": "300",
		},
		{
			"label": _("Number of products"),
			"fieldname": "prod_num",
			"align": "left"
		},
		{
			"label": _("Reference"),
			"fieldname": "reference",
			"width": "500"
		},
	]


def get_data():
	db_name = frappe.conf.get("db_name")

	raw_result = frappe.db.sql("""
	SELECT
		`f`.`name`
		,`f`.`title` AS `function`
		, COUNT(`prod`.`name`) AS `prod_num`
		, `fg`.`title` AS `function_group`
		, `f`.`reference`
	FROM `{}`.`tabDC_PLC_Product_Function` AS `f`
	LEFT JOIN `{}`.`tabDC_PLC_Product_Summary` AS `prod` ON `prod`.`link_function` = `f`.`name`
	INNER JOIN `{}`.`tabDC_PLC_Product_Function_Group` AS `fg` ON `f`.`link_group` = `fg`.`name`
	GROUP BY `f`.`name`
	ORDER BY `fg`.`title` ASC, `f`.`title` ASC;
	""".format(db_name, db_name, db_name), as_list=1)

	result = [prepare_function_filter_row(row) for row in raw_result]

	return result


def prepare_function_filter_row(data):
	id_, title, number, group, ref = data
	return [group, '{}|{}'.format(id_,title), number, ref]
