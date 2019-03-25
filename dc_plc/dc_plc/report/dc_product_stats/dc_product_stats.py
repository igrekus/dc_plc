# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_product_stats(filters)

	return columns, data


def get_columns():
	# return ["#:Data:50", _("Product") + ":Link/DC_PLC_Product_Summary:200", _("Type") + ":Link/PLC_Product_Type:100"]
	return ["ID:Link/DC_PLC_Product_Summary", "Внешний №", "Тип", "ОКР", "Консультанты", "Разработчики", "Кристалл", "Плата в сборке", "Корпус", "Функция", "Применение", "Описание", "Параметры", "ТУ", "Аналоги", "Отчёты", "Даташит"]


def get_product_stats(filters):

	def add_devs_and_cons(row):
		row[4] = cons[row[0]].replace(',', '<br>')
		row[5] = devs[row[0]].replace(',', '<br>')
		return row

	devs = {res[0]: res[1] for res in frappe.db.sql(
"""SELECT t.parent,
       GROUP_CONCAT(CONCAT(emp.last_name, " ", emp.first_name, " ", emp.middle_name)) AS developers
FROM `_1bd3e0294da19198`.`tabDC_PLC_Developers_in_Product` AS t
INNER JOIN `_1bd3e0294da19198`.`tabEmployee` AS emp
ON t.link_employee = emp.employee
GROUP BY t.parent;"""
	)}

	cons = {res[0]: res[1] for res in frappe.db.sql(
"""SELECT t.parent,
       GROUP_CONCAT(CONCAT(emp.last_name, " ", emp.first_name, " ", emp.middle_name)) AS developers
FROM `_1bd3e0294da19198`.tabDC_PLC_Consulants_in_Product AS t
INNER JOIN `_1bd3e0294da19198`.`tabEmployee` AS emp
ON t.link_employee = emp.employee
GROUP BY t.parent;"""
	)}

	result = frappe.db.sql("""SELECT
  p.name as `id`
     , p.ext_num
     , type.title
     , proj.title
     , "stub"
     , "stub"
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

	result = [add_devs_and_cons(row) for row in result]

	return result
