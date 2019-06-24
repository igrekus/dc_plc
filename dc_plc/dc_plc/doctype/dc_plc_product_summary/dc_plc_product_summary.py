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

	return '{}'.format(date)


@frappe.whitelist()
def set_rnd_spec_relevant(name, relevant):
	relevant = int(relevant)
	date = today() if relevant else '0001-01-01'
	doc = frappe.get_doc('DC_PLC_Product_Summary', name)
	doc.rel_check_rnd_spec = relevant
	doc.rel_date_rnd_spec = date
	doc.save()

	return '{}'.format(date)
