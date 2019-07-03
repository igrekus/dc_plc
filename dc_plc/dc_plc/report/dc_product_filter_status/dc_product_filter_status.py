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
		`status`.`name` AS `name`
		,`status`.`title` AS `title`
		, COUNT(`status`.`name`) AS `prod_num`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Status` AS `status` ON `p`.`link_status` = `status`.`name`
	GROUP BY `status`.`name`
	ORDER BY `status`.`title` ASC;""".format(db_name, db_name), as_list=1)

	result = [prepare_status_filter_row(row, host) for row in raw_result]

	return result


def prepare_status_filter_row(data, host):
	id_, title, number = data
	return ['<a href="{}/desk#query-report/DC%20Product%20Stats/Report?link_status={}">{}</a>'.format(host, id_, title), number]
