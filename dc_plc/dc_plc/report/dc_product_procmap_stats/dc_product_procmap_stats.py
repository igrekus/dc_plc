# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from dc_plc.custom.utils import add_product_summary_links, add_completeness, add_query_relevance
from dc_plc.controllers.stats_query import get_procmap_stats


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
		_("Function"),
		_("External number"),
		_("Process map"),
		_("Internal number")
	]


def get_data(filters):
	host = frappe.utils.get_url()
	res = get_procmap_stats(filters)
	has_perms = frappe.has_permission(doctype='DC_PLC_Product_Summary', ptype='write', throw=False, verbose=False)

	res = [add_completeness(row, [4]) for row in res]
	res = [add_query_relevance(row, has_perms) for row in res]
	res = [add_product_summary_links(row, host=host) for row in res]

	return res
