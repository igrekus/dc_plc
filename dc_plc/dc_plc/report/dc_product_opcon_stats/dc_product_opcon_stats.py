# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from dc_plc.custom.utils import add_product_summary_links, add_translation, add_completeness
from dc_plc.controllers.stats_query import get_opcon_stats


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
		_("External number"),
		_("Opcon"),
		_("Internal number")
	]


def get_data(filters):
	result = get_opcon_stats(filters)
	host = frappe.utils.get_url()
	return [add_product_summary_links(add_translation(add_completeness(row, [5, 6])),
										host=host) for row in result]
