import frappe
from frappe import _


def add_translation(row):
	new_row = list(row)
	status = row[1]
	model = row[4]
	new_row[1] = _(status) if status is not None else None
	new_row[4] = _(model) if model is not None else None
	return new_row


def add_product_summary_links(row, host):
	prod_id = row[0]
	return [prod_id] + ['<a href="{}/desk#Form/DC_PLC_Product_Summary/{}">{}</a>'.format(host, prod_id, col) if col is not None else '' for col in row[1:]]
