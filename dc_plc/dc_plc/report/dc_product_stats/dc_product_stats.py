# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from dc_plc.custom.utils import add_product_summary_links, add_translation


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
		_("Status"),
		_("External number"),
		_("Internal number"),
		_("Model"),
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
		_("Analogs"),
		_("Desdoc number"),
		_("Opcon"),
		_("Reports"),
		_("Datasheet")
	]


def get_product_stats(filters):

	# TODO sanitize filters

	def add_devs_and_cons(row):
		row[7] = cons.get(row[0], '').replace(',', '<br>')
		row[8] = devs.get(row[0], '').replace(',', '<br>')
		return row

	db_name = frappe.conf.get("db_name")
	host = frappe.utils.get_url()

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

	sql = """SELECT
       `p`.`name` as `id`
     , `p`.`sel_status`
     , `p`.`ext_num`
     , `p`.`int_num`
     , `p`.`sel_model`
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
     , `p`.`analog`
     , `p`.`desdoc_num`
     , `p`.`opcon`
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
  `{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`"""\
		.format(db_name, db_name, db_name, db_name, db_name)

	if filters:
		proj = filters.get('link_rnd_project', '%')
		proj_clause = "(`proj`.`name` LIKE '%' OR `proj`.`name` IS NULL)" if proj == '%' else "`proj`.`name` LIKE '{}'".format(proj)

		type_ = filters.get('link_type', '%')
		type_clause = "(`type`.`name` LIKE '%' OR `type`.`name` IS NULL)" if type_ == '%' else "`type`.`name` LIKE '{}'".format(type_)

		model = filters.get('sel_model', '%')
		model_clause = "(`p`.`sel_model` LIKE '%' OR `p`.sel_model IS NULL)" if model == '%' else "`p`.`sel_model` LIKE '{}'".format(model)

		func = filters.get('link_function', '%')
		func_clause = "(`fun`.`name` LIKE '%' OR `fun`.`name` IS NULL)" if func == '%' else "`fun`.`name` LIKE '{}'".format(func)

		status = filters.get('sel_status', '%')
		status_clause = "(`p`.`sel_status` LIKE '%' OR `p`.sel_status IS NULL)" if status == '%' else "`p`.`sel_status` LIKE '{}'".format(status)

		pack = filters.get('link_package', '%')
		pack_clause = "(`pak`.`name` LIKE '%' OR `pak`.`name` IS NULL)" if pack == '%' else "`pak`.`name` LIKE '{}'".format(pack)

		sql += """
WHERE
{}
AND
{}
AND
{}
AND
{}
AND
{}
AND
{} 
""".format(proj_clause, type_clause, model_clause, func_clause, status_clause, pack_clause)
		frappe.msgprint(str(filters))
		frappe.msgprint(sql)
	result = frappe.db.sql(sql + ';', as_list=1)
	result = [add_product_summary_links(add_translation(add_devs_and_cons(row)), host) for row in result]

	return result
