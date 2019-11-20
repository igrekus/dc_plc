import contextlib
import frappe
import os
import shutil

from dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary import DC_PLC_Product_Summary
from dc_plc.dc_documents.doctype.dc_doc_meta.dc_doc_meta import DC_Doc_Meta
from frappe.core.doctype.file.file import File


@frappe.whitelist()
def search_existing_datasheets(query):
	return search_existing_meta(
		query=query,
		table='tabDC_Doc_Datasheets_in_Datasheet_List',
		type_id='DT001'
	)


@frappe.whitelist()
def search_existing_dev_reports(query):
	return search_existing_meta(
		query=query,
		table='tabDC_Doc_Dev_Report_in_Dev_Report_List',
		type_id='DT002'
	)


@frappe.whitelist()
def search_existing_misc(query):
	return search_existing_meta(
		query=query,
		table='tabDC_Doc_Misc_in_Misc_List',
		type_id='DT003'
	)


@frappe.whitelist()
def search_existing_opcon(query):
	return search_existing_meta(
		query=query,
		table='tabDC_Doc_Opcon_in_Opcon_List',
		type_id='DT004'
	)


@frappe.whitelist()
def search_existing_desdoc(query):
	return search_existing_meta(
		query=query,
		table='tabDC_Doc_Desdoc_in_Desdoc_List',
		type_id='DT005'
	)


def search_existing_meta(query, table, type_id):
	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(f"""
	SELECT DISTINCT 
		`m`.`name`
		, `m`.`title` AS `meta_title`
		, `m`.`note` AS `note`
		, `m`.`attached_file` AS `url`
	FROM `{db_name}`.tabDC_Doc_Meta AS `m`
	INNER JOIN `{db_name}`.`tabDC_Doc_Document_Subtype` AS `s` ON `m`.`link_subtype` = `s`.`name`
	INNER JOIN `{db_name}`.`tabDC_Doc_Document_Type` AS `st` ON `st`.`name` = `s`.`link_doc_type`
	INNER JOIN `{db_name}`.`{table}` AS `l` ON `l`.`link_doc_meta` = `m`.`name`
	INNER JOIN `{db_name}`.`tabDC_PLC_Product_Summary` AS `p` ON `p`.`name` = `l`.`parent`
	WHERE
		`st`.`name` = '{type_id}'
	AND
		(
		`m`.`title` LIKE %(search)s
		OR
		`p`.`int_num` LIKE %(search)s
		OR
		`p`.`ext_num` LIKE %(search)s
		OR
		DATE(`m`.`creation`) < %(date)s
		) 
	LIMIT 50;""", {
		'search': '%{}%'.format(query),
		'date': '{}'.format(query),
	})

	return [
		{
			'label': d[0],
			'value': d[1],
			'note': d[2],
			'file_url': d[3].replace('\n', '<br>')
		}
		for d in res
	]


@frappe.whitelist()
def get_opcon_subtypes():
	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(f"""
	SELECT
		`s`.`name`
		, `s`.`title`
	FROM
		`{db_name}`.tabDC_Doc_Document_Subtype AS `s`
	WHERE
		`s`.`link_doc_type` = 'DT004'
""")

	return [
		{
			'value': d[0],
			'label': d[1],
		}
		for d in res
	]


@frappe.whitelist()
def get_desdoc_subtypes():
	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(f"""
	SELECT
		`s`.`name`
		, `s`.`title`
	FROM
		`{db_name}`.tabDC_Doc_Document_Subtype AS `s`
	WHERE
		`s`.`link_doc_type` = 'DT005'
""")

	return [
		{
			'value': d[0],
			'label': d[1],
		}
		for d in res
	]


@frappe.whitelist()
def upload_file(*args, **kwargs):
	file_type = kwargs['fileType']

	files = frappe.request.files
	if 'file' in files:
		file = files['file']
		content = file.stream.read()
		filename = file.filename

	uploaded_file_name = f'./site1.local/temp/{file_type}-' + frappe.generate_hash('', 10) + '.dat'
	with open(uploaded_file_name, 'wb') as f:
		f.write(content)

	return uploaded_file_name


@frappe.whitelist()
def remove_temp_file(filename):
	with contextlib.suppress(FileNotFoundError):
		os.remove(filename)
	return 'success'


@frappe.whitelist()
def add_datasheet(prod_id, upload, temp_file):
	ds = frappe.parse_json(upload)

	if ds['label']:
		add_existing_datasheet(prod_id, ds)
	else:
		add_new_datasheet(prod_id, ds, temp_file)

	return 'success'


def add_existing_datasheet(prod_id, datasheet):
	# TODO use single query is performance degrading
	doc: DC_PLC_Product_Summary = frappe.get_doc('DC_PLC_Product_Summary', prod_id)
	meta: DC_Doc_Meta = frappe.get_doc('DC_Doc_Meta', datasheet['label'])
	doc_subype = frappe.get_doc('DC_Doc_Document_Subtype', meta.link_subtype)
	doc_type = frappe.get_doc('DC_Doc_Document_Type', doc_subype.link_doc_type)

	doc.append('tab_datasheet', {
		'link_doc_meta': meta.name,
		'doc_type': doc_type.title,
		'doc_subtype': doc_subype.title
	})
	doc.save()

	return True


def add_new_datasheet(prod_id, datasheet, temp_file):
	file_name = temp_file.split('/')[-1]
	target_file = f'{datasheet["file_url"]}{file_name}'
	stored_url = target_file[20:]   # TODO make less hacky

	try:
		shutil.move(temp_file, target_file, copy_function=shutil.copy)
	except PermissionError:
		pass
	file_info = os.stat(target_file)

	new_meta: DC_Doc_Meta = frappe.get_doc({
		'doctype': 'DC_Doc_Meta',
		'title': datasheet['value'],
		'link_subtype': 'DST002',
		'attached_file': stored_url,
		'note': datasheet['note']
	})
	new_meta.insert()

	new_file: File = frappe.get_doc({
		'doctype': 'File',
		'file_name': datasheet['value'],
		'is_private': 0,
		'file_size': file_info.st_size,
		'file_url': stored_url,
		'folder': 'Home/Datasheets',
		'attached_to_doctype': 'DC_Doc_Meta',
		'attached_to_name': new_meta.name,
		'attached_to_field': 'attached_file',
	})
	new_file.insert()

	add_existing_datasheet(prod_id, datasheet={'label': new_meta.name})

	return True


@frappe.whitelist()
def add_dev_report(prod_id, upload, temp_file):
	ds = frappe.parse_json(upload)

	if ds['label']:
		add_existing_dev_report(prod_id, ds)
	else:
		add_new_dev_report(prod_id, ds, temp_file)

	return 'success'


def add_existing_dev_report(prod_id, dev_report):
	doc: DC_PLC_Product_Summary = frappe.get_doc('DC_PLC_Product_Summary', prod_id)
	meta: DC_Doc_Meta = frappe.get_doc('DC_Doc_Meta', dev_report['label'])
	doc_subype = frappe.get_doc('DC_Doc_Document_Subtype', meta.link_subtype)
	doc_type = frappe.get_doc('DC_Doc_Document_Type', doc_subype.link_doc_type)

	doc.append('tab_dev_report', {
		'link_doc_meta': meta.name,
		'doc_type': doc_type.title,
		'doc_subtype': doc_subype.title,
	})
	doc.save()

	return True


def add_new_dev_report(prod_id, dev_report, temp_file):
	file_name = temp_file.split('/')[-1]
	target_file = f'{dev_report["file_url"]}{file_name}'
	stored_url = target_file[20:]

	try:
		shutil.move(temp_file, target_file, copy_function=shutil.copy)
	except PermissionError:
		pass
	file_info = os.stat(target_file)

	new_meta: DC_Doc_Meta = frappe.get_doc({
		'doctype': 'DC_Doc_Meta',
		'title': dev_report['value'],
		'link_subtype': 'DST003',
		'attached_file': stored_url,
		'note': dev_report['note']
	})
	new_meta.insert()

	new_file: File = frappe.get_doc({
		'doctype': 'File',
		'file_name': dev_report['value'],
		'is_private': 0,
		'file_size': file_info.st_size,
		'file_url': stored_url,
		'folder': 'Home/Developer_Reports',
		'attached_to_doctype': 'DC_Doc_Meta',
		'attached_to_name': new_meta.name,
		'attached_to_field': 'attached_file',
	})
	new_file.insert()

	add_existing_dev_report(prod_id, dev_report={'label': new_meta.name})

	return True


@frappe.whitelist()
def add_misc(prod_id, upload, temp_file):
	ds = frappe.parse_json(upload)

	if ds['label']:
		add_existing_misc(prod_id, ds)
	else:
		add_new_misc(prod_id, ds, temp_file)

	return 'success'


def add_existing_misc(prod_id, misc):
	doc: DC_PLC_Product_Summary = frappe.get_doc('DC_PLC_Product_Summary', prod_id)
	meta: DC_Doc_Meta = frappe.get_doc('DC_Doc_Meta', misc['label'])
	doc_subype = frappe.get_doc('DC_Doc_Document_Subtype', meta.link_subtype)
	doc_type = frappe.get_doc('DC_Doc_Document_Type', doc_subype.link_doc_type)

	doc.append('tab_misc', {
		'link_doc_meta': meta.name,
		'doc_type': doc_type.title,
		'doc_subtype': doc_subype.title,
	})
	doc.save()

	return True


def add_new_misc(prod_id, misc_file, temp_file):
	file_name = temp_file.split('/')[-1]
	target_file = f'{misc_file["file_url"]}{file_name}'
	stored_url = target_file[20:]

	try:
		shutil.move(temp_file, target_file, copy_function=shutil.copy)
	except PermissionError:
		pass
	file_info = os.stat(target_file)

	new_misc: DC_Doc_Meta = frappe.get_doc({
		'doctype': 'DC_Doc_Meta',
		'title': misc_file['value'],
		'link_subtype': 'DST004',
		'attached_file': stored_url,
		'note': misc_file['note']
	})
	new_misc.insert()

	new_file: File = frappe.get_doc({
		'doctype': 'File',
		'file_name': misc_file['value'],
		'is_private': 0,
		'file_size': file_info.st_size,
		'file_url': stored_url,
		'folder': 'Home/Misc_Files',
		'attached_to_doctype': 'DC_Doc_Meta',
		'attached_to_name': new_misc.name,
		'attached_to_field': 'attached_file',
	})
	new_file.insert()

	add_existing_misc(prod_id, misc={'label': new_misc.name})

	return True


@frappe.whitelist()
def add_opcon(prod_id, upload, temp_file):
	ds = frappe.parse_json(upload)

	if ds['label']:
		add_existing_opcon(prod_id, ds)
	else:
		add_new_opcon(prod_id, ds, temp_file)

	return 'success'


def add_existing_opcon(prod_id, opcon):
	doc: DC_PLC_Product_Summary = frappe.get_doc('DC_PLC_Product_Summary', prod_id)
	meta: DC_Doc_Meta = frappe.get_doc('DC_Doc_Meta', opcon['label'])
	doc_subype = frappe.get_doc('DC_Doc_Document_Subtype', meta.link_subtype)
	doc_type = frappe.get_doc('DC_Doc_Document_Type', doc_subype.link_doc_type)

	doc.append('tab_opcon', {
		'link_doc_meta': meta.name,
		'doc_type': doc_type.title,
		'doc_subtype': doc_subype.title,
	})
	doc.save()

	return True


def add_new_opcon(prod_id, opcon_meta, temp_file):
	file_name = temp_file.split('/')[-1]
	target_file = f'{opcon_meta["file_url"]}{file_name}'
	stored_url = target_file[20:]

	try:
		shutil.move(temp_file, target_file, copy_function=shutil.copy)
	except PermissionError:
		pass
	file_info = os.stat(target_file)

	new_opcon: DC_Doc_Meta = frappe.get_doc({
		'doctype': 'DC_Doc_Meta',
		'title': opcon_meta['value'],
		'attached_file': stored_url,
		'link_subtype': opcon_meta['subtype'],
		'note': opcon_meta['note'],
		'opcon_num': opcon_meta['opconNum'],
		'opcon_int_num': opcon_meta['opconIntNum'],
		'date_approve': opcon_meta['dateApproval'][:10],
		'date_archive': opcon_meta['dateArchive'][:10],
	})
	new_opcon.insert()

	new_file: File = frappe.get_doc({
		'doctype': 'File',
		'file_name': opcon_meta['value'],
		'is_private': 0,
		'file_size': file_info.st_size,
		'file_url': stored_url,
		'folder': 'Home/Opcons',
		'attached_to_doctype': 'DC_Doc_Meta',
		'attached_to_name': new_opcon.name,
		'attached_to_field': 'attached_file',
	})
	new_file.insert()

	add_existing_opcon(prod_id, opcon={'label': new_opcon.name})

	return True


@frappe.whitelist()
def add_desdoc(prod_id, upload, temp_file):
	ds = frappe.parse_json(upload)

	if ds['label']:
		add_existing_desdoc(prod_id, ds)
	else:
		add_new_desdoc(prod_id, ds, temp_file)

	return 'success'


def add_existing_desdoc(prod_id, desdoc):
	doc: DC_PLC_Product_Summary = frappe.get_doc('DC_PLC_Product_Summary', prod_id)
	meta: DC_Doc_Meta = frappe.get_doc('DC_Doc_Meta', desdoc['label'])
	doc_subype = frappe.get_doc('DC_Doc_Document_Subtype', meta.link_subtype)
	doc_type = frappe.get_doc('DC_Doc_Document_Type', doc_subype.link_doc_type)

	doc.append('tab_desdoc', {
		'link_doc_meta': meta.name,
		'doc_type': doc_type.title,
		'doc_subtype': doc_subype.title,
	})
	doc.save()

	return True


def add_new_desdoc(prod_id, desdoc_meta, temp_file):
	file_name = temp_file.split('/')[-1]
	target_file = f'{desdoc_meta["file_url"]}{file_name}'
	stored_url = target_file[20:]

	try:
		shutil.move(temp_file, target_file, copy_function=shutil.copy)
	except PermissionError:
		pass
	file_info = os.stat(target_file)

	new_desdoc: DC_Doc_Meta = frappe.get_doc({
		'doctype': 'DC_Doc_Meta',
		'title': desdoc_meta['value'],
		'attached_file': stored_url,
		'link_subtype': desdoc_meta['subtype'],
		'note': desdoc_meta['note'],
		'desdoc_num': desdoc_meta['opconNum'],
		'date_archive': desdoc_meta['dateArchive'][:10],
	})
	new_desdoc.insert()

	new_file: File = frappe.get_doc({
		'doctype': 'File',
		'file_name': desdoc_meta['value'],
		'is_private': 0,
		'file_size': file_info.st_size,
		'file_url': stored_url,
		'folder': 'Home/Design_Documents',
		'attached_to_doctype': 'DC_Doc_Meta',
		'attached_to_name': new_desdoc.name,
		'attached_to_field': 'attached_file',
	})
	new_file.insert()

	add_existing_desdoc(prod_id, desdoc={'label': new_desdoc.name})

	return True
