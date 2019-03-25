# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data()

	return columns, data


def get_columns():
	return [
		"ID:Link/DC_PLC_Product_Summary",
		_("External number"),
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
	return 	frappe.db.sql("""SELECT
  p.name as `id`
     , p.ext_num
     , type.title
     , p.chip
     , p.asm_board
     , pak.title
     , fun.title
     , p.application
     , p.description
     , p.specs
     , p.analog
FROM `_1bd3e0294da19198`.tabDC_PLC_Product_Summary AS p
INNER JOIN `_1bd3e0294da19198`.tabDC_PLC_Product_Type AS type,
           `_1bd3e0294da19198`.tabDC_PLC_RND_Project AS proj,
           `_1bd3e0294da19198`.tabDC_PLC_Package AS pak,
           `_1bd3e0294da19198`.tabDC_PLC_Product_Function AS fun;""", as_list=1)

