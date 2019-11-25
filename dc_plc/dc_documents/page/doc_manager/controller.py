import frappe
from dc_plc.dc_documents.doctype.dc_doc_meta.dc_doc_meta import DC_Doc_Meta
from dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary import DC_PLC_Product_Summary

list_tables = {
	'DT001': 'tabDC_Doc_Datasheets_in_Datasheet_List',
	'DT002': 'tabDC_Doc_Dev_Report_in_Dev_Report_List',
	'DT003': 'tabDC_Doc_Misc_in_Misc_List',
	'DT004': 'tabDC_Doc_Opcon_in_Opcon_List',
	'DT005': 'tabDC_Doc_Desdoc_in_Desdoc_List',
}

list_child_fields = {
	'DT001': 'tab_datasheet',
	'DT002': 'tab_dev_report',
	'DT003': 'tab_misc',
	'DT004': 'tab_opcon',
	'DT005': 'tab_desdoc',
}


@frappe.whitelist()
def get_document_list(filters=None):
	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(f"""
SELECT `m`.`name`
, `m`.`title`
, `st`.`title` AS `subtype`
, `m`.`int_num`
, `m`.`ext_num`
, 'links'
, `t`.`name`
FROM `{db_name}`.`tabDC_Doc_Meta` AS `m`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Subtype` AS `st` ON `m`.`link_subtype` = `st`.`name`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Type` AS `t` ON `t`.`name` = `st`.`link_doc_type`
ORDER BY `subtype` ASC, `title` ASC""")

	return [{
		'id': row[0],
		'filename': row[1],
		'subtype': row[2],
		'int_num': row[3],
		'ext_num': row[4],
		'prod_links': row[5],
		'type_id': row[6]
	} for row in res]


@frappe.whitelist()
def get_doc_meta(id_, type_id):
	db_name = frappe.conf.get("db_name")

	table = list_tables[type_id]

	res = frappe.db.sql(f"""
SELECT `m`.`name`
, `m`.`title`
, `t`.`name` AS `type`
, `st`.`name` AS `subtype`
, `m`.`note`
, `m`.`int_num`
, `m`.`ext_num`
, `m`.`date_approve`
, `m`.`date_archive`
, GROUP_CONCAT(`ml`.`parent`, ',') AS `prod_links`
FROM `{db_name}`.`tabDC_Doc_Meta` AS `m`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Subtype` AS `st` ON `m`.`link_subtype` = `st`.`name`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Type` AS `t` ON `t`.`name` = `st`.`link_doc_type`
INNER JOIN `{db_name}`.`{table}` AS `ml` on `ml`.`link_doc_meta` = `m`.`name`
WHERE `m`.`name` = '{id_}'
GROUP BY `m`.`name`
ORDER BY `subtype` ASC""", as_dict=1)[0]

	return {
		'id': res['name'],
		'name': res['title'],
		'type': res['type'],
		'subtype': res['subtype'],
		'note': res['note'],
		'optional': {
			'num': res['ext_num'],
			'int_num': res['int_num'],
			'date_approve': res['date_approve'],
			'date_archive': res['date_archive'],
		},
		'products': res['prod_links'].strip(',').split(','),
	}


@frappe.whitelist()
def update_document(form_data):
	db_name = frappe.conf.get("db_name")

	form_data = frappe.parse_json(form_data)
	table = list_tables[form_data['type']]
	new_links = set([e for e in form_data['products'] if e])

	res = frappe.db.sql(f"""
SELECT
`ml`.`name`
, `ml`.`parent`
FROM `{db_name}`.`{table}` AS `ml`
WHERE `ml`.`link_doc_meta` = '{form_data['id']}'
GROUP BY `ml`.`parent`
""", as_dict=1)
	existing_links = set([e['parent'] for e in res])
	existing_link_ids = {e['parent']: e['name'] for e in res}

	to_remove = existing_links - new_links
	to_add = new_links - existing_links

	remove_links([existing_link_ids[link] for link in to_remove])
	add_links(to_add, form_data['id'], form_data['type'])

	return existing_links


def add_links(product_ids, meta_id, meta_type):
	meta: DC_Doc_Meta = frappe.get_doc('DC_Doc_Meta', meta_id)
	doc_subype = frappe.get_doc('DC_Doc_Document_Subtype', meta.link_subtype)
	doc_type = frappe.get_doc('DC_Doc_Document_Type', doc_subype.link_doc_type)

	for id_ in product_ids:
		product: DC_PLC_Product_Summary = frappe.get_doc('DC_PLC_Product_Summary', id_)

		product.append(list_child_fields[meta_type], {
			'link_doc_meta': meta.name,
			'doc_type': doc_type.title,
			'doc_subtype': doc_subype.title,
		})
		product.save()

	return True

