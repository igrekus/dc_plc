# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_product_stats(filters)

	return columns, data


def get_columns():
	# return ["#:Data:50", _("Product") + ":Link/DC_PLC_Product_Summary:200", _("Type") + ":Link/PLC_Product_Type:100"]
	return ["ID:Link/DC_PLC_Product_Summary", "Ext number", "Type", "R&D", "Chip", "Board", "Package", "Function", "Application", "Description", "Specs", "Opcon", "Analogs", "Reports", "Datasheet"]


def get_product_stats(filters):
	result = frappe.db.sql("""SELECT
  p.name as `id`
     , p.ext_num
     , type.title
     , proj.title
     , p.chip
     , p.asm_board
     , pak.title
     , fun.title
     , p.application
     , p.description
     , p.specs
     , p.opcon
     , p.analog
     , p.report
     , p.datasheet
FROM `_1bd3e0294da19198`.tabDC_PLC_Product_Summary AS p
INNER JOIN `_1bd3e0294da19198`.tabDC_PLC_Product_Type AS type,
           `_1bd3e0294da19198`.tabDC_PLC_RND_Project AS proj,
           `_1bd3e0294da19198`.tabDC_PLC_Package AS pak,
           `_1bd3e0294da19198`.tabDC_PLC_Product_Function AS fun;""", as_list=1)

	return result
