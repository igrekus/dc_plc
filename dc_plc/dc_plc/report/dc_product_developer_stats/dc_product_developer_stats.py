# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from dc_plc.custom.utils import add_product_summary_links, add_translation, add_completeness


def execute(filters=None):
	columns = get_columns()
	data = get_data()

	return columns, data


def get_columns():
	return [
		"ID:Link/DC_PLC_Product_Summary",
		_("Progress"),
		_("RnD Title"),
		_("Type"),
		_("Model"),
		_("Function"),
		_("Chip"),
		_("Assembly board"),
		_("Package"),
		_("Description"),
		_("Specs"),
		_("Report"),
		_("Analogs"),
		_("External number"),
		_("Internal number"),
	]


def get_data():
	db_name = frappe.conf.get("db_name")
	host = frappe.utils.get_url()

	result = frappe.db.sql("""SELECT
       `p`.`name` as `id`
     , `proj`.`title`

     , `type`.`title`
     , `p`.`sel_model`
     , `fun`.`title`
     , `p`.`chip`
     , `p`.`asm_board`
     , `pak`.`title`
     , `p`.`description`
     , `p`.`specs`
     , `p`.`report`
     , `p`.`analog`
     
     , `p`.`ext_num`
     , `p`.`int_num`
FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
LEFT JOIN
  `{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
LEFT JOIN
  `{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
LEFT JOIN
  `{}`.`tabDC_PLC_Package` AS `pak` ON `p`.`link_package` = `pak`.`name`
LEFT JOIN
  `{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`;""".format(db_name, db_name, db_name, db_name, db_name), as_list=1)

	return [add_product_summary_links(add_translation(add_completeness(row, range(2, 12))), host) for row in result]
