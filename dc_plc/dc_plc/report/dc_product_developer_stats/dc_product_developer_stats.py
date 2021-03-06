# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from dc_plc.custom.utils import add_completeness, add_query_relevance, add_newline
from dc_plc.controllers.stats_query import get_developer_stats, get_developers_for_product, get_consultants_for_product


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	return [
		"ID:Link/DC_PLC_Product_Summary",
		_("Relevance"),
		_("Progress"),
		_("RnD Title"),
		_("Consultants"),
		_("Developers"),
		_("Type"),
		_("Letter"),
		_("Function"),
		_("Chip"),
		_("Assembly board"),
		_("Package"),
		_("Description") + ":Data:300",
		_("Specs") + ":Data:300",
		_("Report"),
		_("Analogs") + ":Data:200",
		_("External number"),
		_("Internal number"),
	]


def get_data(filters):

	def add_devs_and_cons(row):
		row[2] = cons.get(row[0], '').replace(',', '<br>')
		row[3] = devs.get(row[0], '').replace(',', '<br>')
		return row

	def add_dept_head_relevance(row):
		relevant = int(row[-1])
		row[1] += f';{relevant}'
		return row[:-1]

	devs = get_developers_for_product()
	cons = get_consultants_for_product()

	has_perms = 'DC_PLC_Developer' in frappe.get_roles(frappe.session.user)

	res = get_developer_stats(filters)
	res = [add_devs_and_cons(row) for row in res]
	res = [add_completeness(row, range(2, 12)) for row in res]
	res = [add_query_relevance(row, has_perms) for row in res]
	res = [add_dept_head_relevance(row) for row in res]
	res = [add_newline(row) for row in res]

	return res
