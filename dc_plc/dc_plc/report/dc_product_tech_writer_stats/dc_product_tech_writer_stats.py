# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from dc_plc.custom.utils import add_product_summary_links, add_completeness, add_query_relevance
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
		_("Description"),
		_("Specs"),
		_("Reports"),
		_("Analogs"),
		_("External number"),
		_("Internal number"),
		_("Application"),
		_("Datasheet")
	]


def get_data(filters):
	host = frappe.utils.get_url()
	res = get_tech_writer_stats(filters)

	has_perms = 'DC_PLC_Tech_Writer' in frappe.get_roles(frappe.session.user)

	res = [add_completeness(row, [9, 10]) for row in res]
	res = [add_query_relevance(row, has_perms) for row in res]
	res = [add_product_summary_links(row, host) for row in res]

	return res
