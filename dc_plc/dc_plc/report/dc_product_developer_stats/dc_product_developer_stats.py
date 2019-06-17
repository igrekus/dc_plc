# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from dc_plc.custom.utils import add_product_summary_links, add_translation, add_completeness
from dc_plc.controllers.stats_query import get_developer_stats


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	return [
		"ID:Link/DC_PLC_Product_Summary",
		_("Progress"),
		_("RnD Title"),
		_("Type"),
		_("Model"),
		_("Function"),
		_("Chip"),
		_("Assembly board"),
		_("Package"),
		_("Description"),
		_("Specs"),
		_("Report"),
		_("Analogs"),
		_("External number"),
		_("Internal number"),
	]


def get_data(filters):
	host = frappe.utils.get_url()
	result = get_developer_stats(filters)
	return [add_product_summary_links(add_translation(add_completeness(row, range(2, 12))), host) for row in result]
