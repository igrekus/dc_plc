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
			"fieldname": "step",
			"label": _("Lifecycle step"),
			"width": "500",
		},
		{
			"fieldname": "prod_num",
			"label": _("Number of products"),
			"align": "left",
		},
	]


def get_data():
	db_name = frappe.conf.get("db_name")

	raw_result = frappe.db.sql(f"""
SELECT CONCAT(`mil`.`index`, '.', `sg`.`index`, '.', `st`.`index`, ' ', `st`.`title`) AS `step`
, COUNT(`p`.`name`) AS `prod_num`
FROM `tabDC_PLC_Product_Step` AS `st`
LEFT JOIN `tabDC_PLC_Product_Summary` AS `p` ON `p`.`link_step` = `st`.`name`
INNER JOIN `tabDC_PLC_Product_Stage` AS `sg` ON `sg`.`name` = `st`.`link_stage`
INNER JOIN `tabDC_PLC_Product_Milestone` AS `mil` ON `mil`.`name` = `sg`.`link_milestone`
GROUP BY `st`.`name`
ORDER BY `mil`.`index` ASC, `sg`.`index` ASC, `st`.`index` ASC;
""", as_list=1)

	# result = [prepare_function_filter_row(row) for row in raw_result]
	result = raw_result

	return result


def prepare_function_filter_row(data):
	id_, title, number, group, ref = data
	return [group, '{}|{}'.format(title,id_), number, ref]
