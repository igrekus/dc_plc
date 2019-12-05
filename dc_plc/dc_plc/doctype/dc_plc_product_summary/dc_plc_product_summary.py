# -*- coding: utf-8 -*-
# Copyright (c) 2018, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.data import today


class DC_PLC_Product_Summary(Document):
	pass


# TODO DRY this crap
@frappe.whitelist()
def set_dept_head_relevant(name, relevant):
	relevant = int(relevant)
	date = today() if relevant else '0001-01-01'
	doc = frappe.get_doc('DC_PLC_Product_Summary', name)
	doc.rel_check_dept_head = relevant
	doc.rel_date_dept_head = date
	doc.save()

	return {'date': date, 'check': relevant}


@frappe.whitelist()
def set_rnd_spec_relevant(name, relevant):
	relevant = int(relevant)
	date = today() if relevant else '0001-01-01'
	doc = frappe.get_doc('DC_PLC_Product_Summary', name)
	doc.rel_check_rnd_spec = relevant
	doc.rel_date_rnd_spec = date
	doc.save()

	return {'date': date, 'check': relevant}


@frappe.whitelist()
def set_developer_relevant(name, relevant):
	relevant = int(relevant)
	date = today() if relevant else '0001-01-01'
	doc = frappe.get_doc('DC_PLC_Product_Summary', name)
	doc.rel_check_developer = relevant
	doc.rel_date_developer = date
	doc.save()

	return {'date': date, 'check': relevant}


@frappe.whitelist()
def set_opcon_relevant(name, relevant):
	relevant = int(relevant)
	date = today() if relevant else '0001-01-01'
	doc = frappe.get_doc('DC_PLC_Product_Summary', name)
	doc.rel_check_opcon = relevant
	doc.rel_date_opcon = date
	doc.save()

	return {'date': date, 'check': relevant}


@frappe.whitelist()
def set_procmap_relevant(name, relevant):
	relevant = int(relevant)
	date = today() if relevant else '0001-01-01'
	doc = frappe.get_doc('DC_PLC_Product_Summary', name)
	doc.rel_check_procmap = relevant
	doc.rel_date_procmap = date
	doc.save()

	return {'date': date, 'check': relevant}


@frappe.whitelist()
def set_tech_writer_relevant(name, relevant):
	relevant = int(relevant)
	date = today() if relevant else '0001-01-01'
	doc = frappe.get_doc('DC_PLC_Product_Summary', name)
	doc.rel_check_tech_writer = relevant
	doc.rel_date_tech_writer = date
	doc.save()

	return {'date': date, 'check': relevant}


@frappe.whitelist()
def set_desdoc_relevant(name, relevant):
	relevant = int(relevant)
	date = today() if relevant else '0001-01-01'
	doc = frappe.get_doc('DC_PLC_Product_Summary', name)
	doc.rel_check_desdoc = relevant
	doc.rel_date_desdoc = date
	doc.save()

	return {'date': date, 'check': relevant}


@frappe.whitelist()
def get_step_info(prod_id):
	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(
		query=f"""
SELECT CONCAT(`mil`.`index`, '.', `stg`.`index`, '.', `stp`.`index`, ' ', `stp`.`title`) AS step
FROM `{db_name}`.`tabDC_PLC_Product_Summary` AS `p`
INNER JOIN `{db_name}`.`tabDC_PLC_Product_Step` AS `stp` ON `stp`.`name` = `p`.`link_step`
INNER JOIN `{db_name}`.`tabDC_PLC_Product_Stage` AS `stg` ON `stg`.`name` = `stp`.`link_stage`
INNER JOIN `{db_name}`.`tabDC_PLC_Product_Milestone` AS `mil` ON `mil`.`name` = `stg`.`link_milestone`
WHERE `p`.`name` = %(id)s;""",
		values={
			'id': f'{prod_id}'
		})
	try:
		res = res[0][0]
	except IndexError:
		res = '-'
	return res
