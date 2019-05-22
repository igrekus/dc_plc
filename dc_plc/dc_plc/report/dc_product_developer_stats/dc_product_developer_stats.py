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
		_("Status"),
		_("External number"),
		_("Internal number"),
		_("BKVP Number"),
		_("Model"),
		_("Type"),
		_("Chip"),
		_("Assembly board"),
		_("Package"),
		_("Function"),
		_("Application"),
		_("Description"),
		_("Specs"),
		_("Analogs"),
	]


def get_data():

	def add_links(row):
		prod_id = row[0]
		return [prod_id] + ['<a href="{}/desk#Form/DC_PLC_Product_Summary/{}">{}</a>'.format(host, prod_id, col) if col is not None else '' for col in row[1:]]

	db_name = frappe.conf.get("db_name")
	host = frappe.utils.get_url()

	result = frappe.db.sql("""SELECT
       `p`.`name` as `id`
     , `p`.`sel_status`
     , `p`.`ext_num`
     , `p`.`int_num`
     , bkvp.`title`
     , `p`.`sel_model`
     , type.title
     , p.chip
     , p.asm_board
     , pak.title
     , fun.title
     , p.application
     , p.description
     , p.specs
     , p.analog
FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
LEFT JOIN
  `{}`.`tabDC_PLC_BKVP_Number` AS `bkvp` ON `p`.`link_bkvp_num` = `bkvp`.`name`
LEFT JOIN
  `{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
LEFT JOIN
  `{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
LEFT JOIN
  `{}`.`tabDC_PLC_Package` AS `pak` ON `p`.`link_package` = `pak`.`name`
LEFT JOIN
  `{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`;""".format(db_name, db_name, db_name, db_name, db_name, db_name), as_list=1)

	return [add_links(row) for row in result]
