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
        "ID:Link/DC_PLC_Product_Summary",
        _("External number"),
        _("Internal number"),
        _("Type"),
        _("RnD Title")
    ]


def get_data():
	db_name = frappe.conf.get("db_name")

	result = frappe.db.sql("""SELECT
	  p.name as `id`
	     , p.ext_num
	     , p.int_num
	     , type.title
	     , proj.title
FROM `{}`.tabDC_PLC_Product_Summary AS p
LEFT JOIN
  `{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
LEFT JOIN
  `{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`;""".format(db_name, db_name, db_name), as_list=1)

	return result

