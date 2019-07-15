# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals, division
import frappe
from frappe import _

from dc_plc.custom.utils import add_translation, add_completeness
from dc_plc.controllers.stats_query import get_full_stats, get_developers_for_product, get_consultants_for_product


def execute(filters=None):
	if not filters:
		filters = dict()

	return get_columns(), get_data(filters)


def get_columns():
	return [
		"ID:Link/DC_PLC_Product_Summary",
		_("Relevance"),
		_("Progress"),
		_("Status"),
		_("External number"),
		_("Internal number"),
		_("Letter"),
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
		_("Process map"),
		_("Reports"),
		_("Datasheet"),
		_("Final description")
	]


def get_data(filters):
	# TODO sanitize filters
	# TODO refactor hardcoded indexes

	relevance_values = {
		0: 3,
		1: 1,
		2: 10,
		3: 2,
		4: 1,
		5: 3,
		6: 2
	}
	cell_groups = {
		0: [4, 10, 11],
		1: [9],
		2: [8, 7, 15, 12, 13, 14, 17, 18, 23, 19],
		3: [5, 21],
		4: [22],
		5: [16, 24, 25],
		6: [6, 20],
	}

	def add_devs_and_cons(row):
		row[7] = cons.get(row[0], '').replace(',', '<br>')
		row[8] = devs.get(row[0], '').replace(',', '<br>')
		return row

	def add_relevance(row):
		done = 0
		total = 22
		flags = row[24:]
		cells_to_highlight = list()
		for index, flag in enumerate(flags):
			if flag:
				done += relevance_values[index]
				cells_to_highlight += cell_groups[index]
		percent = int((done/total) * 100)
		return [row[0]] + ['{}|{}%'.format(cells_to_highlight, percent)] + row[1:]

	devs = get_developers_for_product()
	cons = get_consultants_for_product()
	result = get_full_stats(filters)

	result = [add_devs_and_cons(row) for row in result]
	result = [add_completeness(row, range(21)) for row in result]
	result = [add_relevance(row) for row in result]

	return result
