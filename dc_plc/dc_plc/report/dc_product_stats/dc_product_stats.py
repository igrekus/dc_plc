# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from dc_plc.custom.utils import add_product_summary_links, add_translation, add_completeness
from dc_plc.controllers.stats_query import get_full_stats, get_developers_for_product, get_consultants_for_product


def execute(filters=None):
	if not filters:
		filters = dict()

	return get_columns(), get_data(filters)


def get_columns():
	return [
		"ID:Link/DC_PLC_Product_Summary",
		_("Progress"),
		_("Status"),
		_("External number"),
		_("Internal number"),
		_("Model"),
		_("Type"),
		_("RnD Title"),
		_("Consultants"),
		_("Developers"),
		_("Chip"),
		_("Assembly board"),
		_("Package"),
		_("Function"),
		_("Application"),
		_("Description"),
		_("Specs"),
		_("Analogs"),
		_("Desdoc number"),
		_("Opcon"),
		_("Reports"),
		_("Datasheet")
	]


def get_data(filters):
	# TODO sanitize filters

	def add_devs_and_cons(row):
		row[7] = cons.get(row[0], '').replace(',', '<br>')
		row[8] = devs.get(row[0], '').replace(',', '<br>')
		return row

	devs = get_developers_for_product()
	cons = get_consultants_for_product()

	return [add_product_summary_links(add_translation(add_completeness(add_devs_and_cons(row))),
	                                  host=frappe.utils.get_url()) for row in get_full_stats(filters)]
