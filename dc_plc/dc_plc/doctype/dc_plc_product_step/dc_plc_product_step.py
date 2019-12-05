# -*- coding: utf-8 -*-
# Copyright (c) 2019, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe

from frappe.model.document import Document


class DC_PLC_Product_Step(Document):
	pass


@frappe.whitelist()
def get_lifecycle_step_filter(doctype, txt, searchfield, start, page_len, filters):
	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(
		query=f"""SELECT
`st`.`name`  AS `value`
, `st`.`title` AS `label`
FROM `{db_name}`.`tabDC_PLC_Product_Step` AS `st`
WHERE (
	`st`.`name` LIKE %(search)s OR
	`st`.`title` LIKE %(search)s
)""",
		values={
			'search': f'%{txt}%'
		},
		as_list=1)
	return res
