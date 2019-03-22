# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data()

	return columns, data


def get_columns():
	return ["ID:Link/DC_PLC_Product_Summary", "Внешний номер", "Тип", "ОКР"]


def get_data():

	result = frappe.db.sql("""SELECT
	  p.name as `id`
	     , p.ext_num
	     , type.title
	     , proj.title
	FROM `_1bd3e0294da19198`.tabDC_PLC_Product_Summary AS p
	INNER JOIN `_1bd3e0294da19198`.tabDC_PLC_Product_Type AS type,
	           `_1bd3e0294da19198`.tabDC_PLC_RND_Project AS proj;""", as_list=1)

	return result

