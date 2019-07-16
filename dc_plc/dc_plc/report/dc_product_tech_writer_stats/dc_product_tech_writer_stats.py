# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from dc_plc.custom.utils import add_completeness, add_query_relevance, add_newline
from dc_plc.controllers.stats_query import get_tech_writer_stats


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	return [
		"ID:Link/DC_PLC_Product_Summary",
		_("Relevance"),
		_("Progress"),
		_("Function"),
		_("Package"),
		_("Description") + ":Data:300",
		_("Specs") + ":Data:300",
		_("Reports"),
		_("Analogs") + ":Data:200",
		_("External number"),
		_("Internal number"),
		_("Application"),
		_("Datasheet"),
		_("Final description") + ":Data:300"
	]


def get_data(filters):
	res = get_tech_writer_stats(filters)

	has_perms = 'DC_PLC_Tech_Writer' in frappe.get_roles(frappe.session.user)

	res = [add_completeness(row, [9, 10, 11]) for row in res]
	res = [add_query_relevance(row, has_perms) for row in res]
	res = [add_newline(row) for row in res]

	return res
