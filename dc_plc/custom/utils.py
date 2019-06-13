from __future__ import division
from frappe import _


def add_translation(row):
	new_row = list(row)
	status = row[1]
	model = row[4]
	new_row[1] = _(status) if status is not None else None
	new_row[4] = _(model) if model is not None else None
	return new_row


def add_translation_to_col_num(row, cols):
	new_row = list(row)
	for col in cols:
		tmp = row[col]
		new_row[col] = _(tmp) if tmp is not None else None
	return new_row


def add_completeness(row):
	new_row = list(row)
	filled, total = count_filled_fields(row, range(len(row)))
	return [new_row[0]] + [calc_percent(filled, total)] + new_row[1:]


def calc_percent(value, total):
	return int(round(value / total, 2) * 100)


def add_product_summary_links(row, host):
	prod_id = row[0]
	return [prod_id] + ['<a href="{}/desk#Form/DC_PLC_Product_Summary/{}">{}</a>'.format(host, prod_id, col) if col is not None else '' for col in row[1:]]


def prepare_function_filter_row(data, host):
	id_, title, number = data
	return ['<a href="{}/desk#query-report/DC%20Product%20Stats/Report?link_function={}">{}</a>'.format(host, id_, title), number]


def prepare_rnd_project_filter_row(data, host):
	id_, title, number = data
	return ['<a href="{}/desk#query-report/DC%20Product%20Stats/Report?link_rnd_project={}">{}</a>'.format(host, id_, title), number]


def prepare_product_type_filter_row(data, host):
	id_, title, number = data
	return ['<a href="{}/desk#query-report/DC%20Product%20Stats/Report?link_type={}">{}</a>'.format(host, id_, title), number]


def prepare_product_package_filter_row(data, host):
	id_, title, number = data
	return ['<a href="{}/desk#query-report/DC%20Product%20Stats/Report?link_package={}">{}</a>'.format(host, id_, title), number]


def prepare_model_filter_row(data, host):
	id_, title, number = data
	return ['<a href="{}/desk#query-report/DC%20Product%20Stats/Report?sel_model={}">{}</a>'.format(host, id_, title), number]


def prepare_status_filter_row(data, host):
	id_, title, number = data
	return ['<a href="{}/desk#query-report/DC%20Product%20Stats/Report?sel_status={}">{}</a>'.format(host, id_, title), number]


def count_filled_fields(row, indexes):
	total = 0
	for index in indexes:
		if row[index]:
			total += 1
	return total, len(row)
