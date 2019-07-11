from __future__ import division
from frappe import _
import frappe


def add_translation(row):
	new_row = list(row)
	status = row[2]
	model = row[5]
	new_row[2] = _(status) if status is not None else None
	new_row[5] = _(model) if model is not None else None
	return new_row


def add_translation_to_col_num(row, cols):
	new_row = list(row)
	for col in cols:
		tmp = row[col]
		new_row[col] = _(tmp) if tmp is not None else None
	return new_row


def add_completeness(row, rows):
	new_row = list(row)
	filled, total = count_filled_fields(row, rows)
	return [new_row[0]] + [str(calc_percent(filled, total)) + "%"] + new_row[1:]


# TODO move page-specific function to respective file
def add_query_relevance(row, has_perms=True):
	relevant = True if row[-2] == 1 else False
	date = row[-1] if row[-1] else '0001-01-01'
	control = '{};{};{}'.format(date, int(relevant), int(has_perms))
	return [row[0]] + [control] + row[1:-2]


def calc_percent(value, total):
	return int(round(value / total, 2) * 100)


def prepare_rnd_project_filter_row(data, host):
	id_, title, number = data
	return ['<a href="{}/desk#query-report/DC%20Product%20Stats/Report?link_rnd_project={}">{}</a>'.format(host, id_, title), number]


def prepare_product_type_filter_row(data, host):
	id_, title, number = data
	return ['<a href="{}/desk#query-report/DC%20Product%20Stats/Report?link_type={}">{}</a>'.format(host, id_, title), number]


def prepare_product_package_filter_row(data, host):
	id_, title, number = data
	return ['<a href="{}/desk#query-report/DC%20Product%20Stats/Report?link_package={}">{}</a>'.format(host, id_, title), number]


def count_filled_fields(row, indexes):
	total = 0
	for index in indexes:
		if row[index] and row[index] != '-':
			total += 1
	return total, len(indexes)
