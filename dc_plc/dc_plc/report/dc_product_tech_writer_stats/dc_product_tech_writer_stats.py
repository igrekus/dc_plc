# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data()
	return columns, data


def get_columns():
	# return ["#:Data:50", _("Product") + ":Link/DC_PLC_Product_Summary:200", _("Type") + ":Link/PLC_Product_Type:100"]
	return [
		"ID:Link/DC_PLC_Product_Summary",
		_("Внешний нормер"),
		_("Описание"),
		_("Параметры"),
		_("Аналоаги"),
		_("Отчёты"),
		_("Даташит")
	]


def get_data():

	result = frappe.db.sql("""SELECT
  p.name as `id`
     , p.ext_num
     , p.description
     , p.specs
     , p.analog
     , p.report
     , p.datasheet
FROM `_1bd3e0294da19198`.tabDC_PLC_Product_Summary AS p;""", as_list=1)

	return result
