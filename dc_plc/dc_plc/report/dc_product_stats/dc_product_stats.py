# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_product_stats(filters)

	return columns, data


def get_columns():
	# return ["#:Data:50", _("Product") + ":Link/DC_PLC_Product_Summary:200", _("Type") + ":Link/PLC_Product_Type:100"]
	return [
		"ID:Link/DC_PLC_Product_Summary",
		_("External number"),
		_("Type"),
		_("RnD Title"),
		_("Consultants"),
		_("Developers"),
		_("Chip"),
		_("Assembly board"),
		_("Package"),
		_("Function"),
		_("Application"),
		_("Description"),
		_("Specs"),
		_("Opcon"),
		_("Analogs"),
		_("Reports"),
		_("Datasheet")
	]


def get_product_stats(filters):

	def add_devs_and_cons(row):
		row[4] = cons.get(row[0], '').replace(',', '<br>')
		row[5] = devs.get(row[0], '').replace(',', '<br>')
		return row

	db_name = frappe.conf.get("db_name")

	devs = {res[0]: res[1] for res in frappe.db.sql(
"""SELECT t.parent,
       GROUP_CONCAT(CONCAT(emp.last_name, " ", emp.first_name, " ", emp.middle_name)) AS developers
       FROM `{}`.`tabDC_PLC_Developers_in_Product` AS t
       INNER JOIN `{}`.`tabEmployee` AS emp
       ON t.link_employee = emp.employee
       GROUP BY t.parent;""".format(db_name, db_name)
	)}

	cons = {res[0]: res[1] for res in frappe.db.sql(
"""SELECT t.parent,
       GROUP_CONCAT(CONCAT(emp.last_name, " ", emp.first_name, " ", emp.middle_name)) AS developers
	   FROM `{}`.tabDC_PLC_Consulants_in_Product AS t
       INNER JOIN `{}`.`tabEmployee` AS emp
       ON t.link_employee = emp.employee
       GROUP BY t.parent;""".format(db_name, db_name)
	)}

	result = frappe.db.sql("""SELECT
       `p`.`name` as `id`
     , `p`.`ext_num`
     , `type`.`title`
     , `proj`.`title`
     , "stub"
     , "stub"
     , `p`.`chip`
     , `p`.`asm_board`
     , `pak`.`title`
     , `fun`.`title`
     , `p`.`application`
     , `p`.`description`
     , `p`.`specs`
     , `p`.`opcon`
     , `p`.`analog`
     , `p`.`report`
     , `p`.`datasheet`
FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
LEFT JOIN
  `{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
LEFT JOIN
  `{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
LEFt JOIN
  `{}`.`tabDC_PLC_Package` AS `pak` ON `p`.`link_package` = `pak`.`name`
LEFT JOIN
  `{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`;"""
						   .format(db_name,db_name,db_name,db_name,db_name), as_list=1)

	result = [add_devs_and_cons(row) for row in result]

	return result
