# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _

from dc_plc.custom.utils import prepare_model_filter_row, add_translation_to_col_num


def execute(filters=None):
	columns = get_columns()
	data = get_data()
	return columns, data


def get_columns():
	return [
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
	]


def get_data():
	db_name = frappe.conf.get("db_name")

	host = frappe.utils.get_url()

	raw_result = frappe.db.sql("""
	SELECT
		`p`.`sel_model` AS `name`
		, `p`.`sel_model` AS `title`
		, COUNT(`p`.`name`) AS `prod_num`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	WHERE `p`.sel_model IS NOT NULL
	GROUP BY `p`.`sel_model`
	ORDER BY `title` ASC;""".format(db_name, db_name), as_list=1)

	result = [prepare_model_filter_row(add_translation_to_col_num(row, [0]), host) for row in raw_result]

	return result
