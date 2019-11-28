import os
import shutil
import frappe

from dc_plc.dc_documents.doctype.dc_doc_meta.dc_doc_meta import DC_Doc_Meta
from dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary import DC_PLC_Product_Summary
from frappe.core.doctype.file.file import File

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

list_folders = {
	'DT001': 'datasheets',
	'DT002': 'dev_reports',
	'DT003': 'misc',
	'DT004': 'opcons',
	'DT005': 'desdocs',
}


list_virtual_folders = {
	'DT001': 'Home/Datasheets',
	'DT002': 'Home/Developer_Reports',
	'DT003': 'Home/Misc_Files',
	'DT004': 'Home/Opcons',
	'DT005': 'Home/Design_Documents',
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
		'prod_links': [],
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
LEFT JOIN `{db_name}`.`{table}` AS `ml` on `ml`.`link_doc_meta` = `m`.`name`
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
		'products': res['prod_links'].strip(',').split(',') if res['prod_links'] else [],
	}


@frappe.whitelist()
def get_doc_links(id_, type_id):
	db_name = frappe.conf.get("db_name")

	table = list_tables[type_id]

	res = frappe.db.sql(f"""SELECT
`m`.`name`
, `p`.`name` AS prod
, `p`.`ext_num`
, `p`.`int_num`
FROM `{db_name}`.`tabDC_Doc_Meta` AS `m`
INNER JOIN `{db_name}`.`{table}` AS `ml` on `ml`.`link_doc_meta` = `m`.`name`
INNER JOIN `{db_name}`.`tabDC_PLC_Product_Summary` AS `p` on `p`.`name` = `ml`.`parent`
WHERE `m`.`name` = '{id_}'
""", as_dict=1)

	return res


@frappe.whitelist()
def add_new_document(form_data):
	# TODO refactor ASAP !!!
	form_data = frappe.parse_json(form_data)

	temp_file = form_data['tempFileName']
	file_name = temp_file.split('/')[-1]
	target_file = f'./site1.local/public/files/{list_folders[form_data["type"]]}/{file_name}'
	stored_url = target_file[20:]

	try:
		shutil.move(temp_file, target_file, copy_function=shutil.copy)
	except PermissionError:
		pass
	file_info = os.stat(target_file)

	date_approve = form_data['optional']['date_approve']
	date_archive = form_data['optional']['date_archive']

	new_meta: DC_Doc_Meta = frappe.get_doc({
		'doctype': 'DC_Doc_Meta',
		'title': form_data['name'],
		'link_subtype': form_data['subtype'],
		'attached_file': stored_url,
		'note': form_data['note'],
		'ext_num': form_data['optional']['num'],
		'int_num': form_data['optional']['int_num'],
		'date_approve': date_approve[:10] if date_approve is not None else None,
		'date_archive': date_archive[:10] if date_archive is not None else None,
	})
	new_meta.insert()

	new_file: File = frappe.get_doc({
		'doctype': 'File',
		'file_name': form_data['name'],
		'is_private': 0,
		'file_size': file_info.st_size,
		'file_url': stored_url,
		'folder': list_virtual_folders[form_data['type']],
		'attached_to_doctype': 'DC_Doc_Meta',
		'attached_to_name': new_meta.name,
		'attached_to_field': 'attached_file',
	})
	new_file.insert()

	to_add = set([e for e in form_data['products'] if e])
	res_add = add_links(to_add, new_meta.name, form_data['type'])
	return ['', res_add]


@frappe.whitelist()
def update_document(form_data):
	# TODO needs refactor badly
	db_name = frappe.conf.get("db_name")

	form_data = frappe.parse_json(form_data)

	existing_meta: DC_Doc_Meta = frappe.get_doc({
		'name': form_data['id'],
		'doctype': 'DC_Doc_Meta',
	})

	date_approve = form_data['optional']['date_approve']
	date_archive = form_data['optional']['date_archive']
	existing_meta.title = form_data['name']
	existing_meta.link_subtype = form_data['subtype']
	existing_meta.note = form_data['note']
	existing_meta.ext_num = form_data['optional']['num']
	existing_meta.int_num = form_data['optional']['int_num']
	existing_meta.date_approve = date_approve[:10] if date_approve is not None else None
	existing_meta.date_date_archive = date_archive[:10] if date_archive is not None else None
	existing_meta.save()

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

	res_remove = remove_links([existing_link_ids[link] for link in to_remove], form_data['id'], form_data['type'])
	res_add = add_links(to_add, form_data['id'], form_data['type'])

	return [res_remove, res_add]


def remove_links(link_ids, meta_id, meta_type):
	if not link_ids:
		return

	# TODO refactor to use the document API
	sql = f"""DELETE FROM `{list_tables[meta_type]}` 
WHERE `name` in ({','.join([f'"{s}"' for s in link_ids])})"""

	return frappe.db.sql(sql)


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

	return len(product_ids)

