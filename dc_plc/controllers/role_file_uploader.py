import contextlib
import frappe
import os
import shutil

from frappe.core.doctype.file.file import File
from dc_plc.dc_documents.doctype.dc_doc_desdoc_meta.dc_doc_desdoc_meta import DC_Doc_Desdoc_Meta
from dc_plc.dc_documents.doctype.dc_doc_misc_meta.dc_doc_misc_meta import DC_Doc_Misc_Meta
from dc_plc.dc_documents.doctype.dc_doc_opcon_meta.dc_doc_opcon_meta import DC_Doc_Opcon_Meta
from dc_plc.dc_documents.doctype.dc_doc_dev_report_meta.dc_doc_dev_report_meta import DC_Doc_Dev_Report_Meta
from dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary import DC_PLC_Product_Summary
from dc_plc.dc_documents.doctype.dc_doc_datasheet_meta.dc_doc_datasheet_meta import DC_Doc_Datasheet_Meta


@frappe.whitelist()
def search_existing_datasheets(query):
	"""
	Search for existing datasheets
	:param query: str -- text search query
	:return: list -- list of {'value': '', 'label': ''} entries
	"""

	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(f"""
SELECT DISTINCT 
	`m`.`name`
	, `m`.`title` AS `meta_title`
	, `m`.`note` AS `note`
	, `m`.`attached_file` AS `url`
FROM
	`{db_name}`.tabDC_Doc_Datasheet_Meta AS `m`
INNER JOIN
	`{db_name}`.tabDC_Doc_Document_Subtype AS `s` ON `m`.`link_subtype` = `s`.`name`
INNER JOIN
	`{db_name}`.tabDC_Doc_Datasheets_in_Datasheet_List AS `l` ON `l`.`link_datasheet_meta` = `m`.`name`
INNER JOIN
	`{db_name}`.tabDC_PLC_Product_Summary AS `p` ON `p`.`name` = `l`.`parent`
WHERE
	`s`.`name` = 'DST002'
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
LIMIT 10;""", {
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
def search_existing_dev_reports(query):
	"""
	Search for existing developer reports
	:param query: str -- text search query
	:return: list -- list of {'value': '', 'label': ''} entries
	"""

	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(f"""
SELECT DISTINCT 
	`m`.`name`
	, `m`.`title` AS `meta_title`
	, `m`.`note` AS `note`
	, `m`.`attached_file` AS `url`
FROM
	`{db_name}`.tabDC_Doc_Dev_Report_Meta AS `m`
INNER JOIN
	`{db_name}`.tabDC_Doc_Document_Subtype AS `s` ON `m`.`link_subtype` = `s`.`name`
INNER JOIN
	`{db_name}`.tabDC_Doc_Dev_Report_in_Dev_Report_List AS `l` ON `l`.`link_dev_report_meta` = `m`.`name`
INNER JOIN
	`{db_name}`.tabDC_PLC_Product_Summary AS `p` ON `p`.`name` = `l`.`parent`
WHERE
	`s`.`name` = 'DST003'
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
LIMIT 10;""", {
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
def search_existing_misc(query):
	"""
	Search for existing developer reports
	:param query: str -- text search query
	:return: list -- list of {'value': '', 'label': ''} entries
	"""

	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(f"""
SELECT DISTINCT 
	`m`.`name`
	, `m`.`title` AS `meta_title`
	, `m`.`note` AS `note`
	, `m`.`attached_file` AS `url`
FROM
	`{db_name}`.tabDC_Doc_Misc_Meta AS `m`
INNER JOIN
	`{db_name}`.tabDC_Doc_Document_Subtype AS `s` ON `m`.`link_subtype` = `s`.`name`
INNER JOIN
	`{db_name}`.tabDC_Doc_Misc_in_Misc_List AS `l` ON `l`.`link_misc_meta` = `m`.`name`
INNER JOIN
	`{db_name}`.tabDC_PLC_Product_Summary AS `p` ON `p`.`name` = `l`.`parent`
WHERE
	`s`.`name` = 'DST004'
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
LIMIT 10;""", {
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
def search_existing_opcon(query):
	"""
	Search for existing opcons
	:param query: str -- text search query
	:return: list -- list of {'value': '', 'label': ''} entries
	"""

	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(f"""
SELECT DISTINCT 
	`m`.`name`
	, `m`.`title` AS `meta_title`
	, `m`.`note` AS `note`
	, `m`.`attached_file` AS `url`
FROM
	`{db_name}`.tabDC_Doc_Opcon_Meta AS `m`
INNER JOIN
	`{db_name}`.tabDC_Doc_Document_Subtype AS `s` ON `m`.`link_subtype` = `s`.`name`
INNER JOIN
	`{db_name}`.tabDC_Doc_Opcon_in_Opcon_List AS `l` ON `l`.`link_opcon_meta` = `m`.`name`
INNER JOIN
	`{db_name}`.tabDC_PLC_Product_Summary AS `p` ON `p`.`name` = `l`.`parent`
WHERE
	`s`.`name` IN ('DST005', 'DST006', 'DST007')
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
LIMIT 10;""", {
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
def search_existing_desdoc(query):
	"""
	Search for existing desdocs
	:param query: str -- text search query
	:return: list -- list of {'value': '', 'label': ''} entries
	"""

	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(f"""
SELECT DISTINCT 
	`m`.`name`
	, `m`.`title` AS `meta_title`
	, `m`.`note` AS `note`
	, `m`.`attached_file` AS `url`
FROM
	`{db_name}`.tabDC_Doc_Desdoc_Meta AS `m`
INNER JOIN
	`{db_name}`.tabDC_Doc_Document_Subtype AS `s` ON `m`.`link_subtype` = `s`.`name`
INNER JOIN
	`{db_name}`.tabDC_Doc_Desdoc_in_Desdoc_List AS `l` ON `l`.`link_desdoc_meta` = `m`.`name`
INNER JOIN
	`{db_name}`.tabDC_PLC_Product_Summary AS `p` ON `p`.`name` = `l`.`parent`
WHERE
	`s`.`name` IN ('DST008', 'DST009', 'DST0010')
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
LIMIT 10;""", {
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
	meta: DC_Doc_Datasheet_Meta = frappe.get_doc('DC_Doc_Datasheet_Meta', datasheet['label'])
	doc_subype = frappe.get_doc('DC_Doc_Document_Subtype', meta.link_subtype)
	doc_type = frappe.get_doc('DC_Doc_Document_Type', doc_subype.link_doc_type)

	doc.append('tab_datasheet', {
		'link_datasheet_meta': meta.name,
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

	new_meta: DC_Doc_Datasheet_Meta = frappe.get_doc({
		'doctype': 'DC_Doc_Datasheet_Meta',
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
		'attached_to_doctype': 'DC_Doc_Datasheet_Meta',
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
	meta: DC_Doc_Dev_Report_Meta = frappe.get_doc('DC_Doc_Dev_Report_Meta', dev_report['label'])
	doc_subype = frappe.get_doc('DC_Doc_Document_Subtype', meta.link_subtype)
	doc_type = frappe.get_doc('DC_Doc_Document_Type', doc_subype.link_doc_type)

	doc.append('tab_dev_report', {
		'link_dev_report_meta': meta.name,
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

	new_meta: DC_Doc_Dev_Report_Meta = frappe.get_doc({
		'doctype': 'DC_Doc_Dev_Report_Meta',
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
		'attached_to_doctype': 'DC_Doc_Dev_Report_Meta',
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
	meta: DC_Doc_Misc_Meta = frappe.get_doc('DC_Doc_Misc_Meta', misc['label'])
	doc_subype = frappe.get_doc('DC_Doc_Document_Subtype', meta.link_subtype)
	doc_type = frappe.get_doc('DC_Doc_Document_Type', doc_subype.link_doc_type)

	doc.append('tab_misc', {
		'link_misc_meta': meta.name,
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

	new_misc: DC_Doc_Misc_Meta = frappe.get_doc({
		'doctype': 'DC_Doc_Misc_Meta',
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
		'attached_to_doctype': 'DC_Doc_Misc_Meta',
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


def add_existing_opcon(prod_id, misc):
	doc: DC_PLC_Product_Summary = frappe.get_doc('DC_PLC_Product_Summary', prod_id)
	meta: DC_Doc_Opcon_Meta = frappe.get_doc('DC_Doc_Opcon_Meta', misc['label'])
	doc_subype = frappe.get_doc('DC_Doc_Document_Subtype', meta.link_subtype)
	doc_type = frappe.get_doc('DC_Doc_Document_Type', doc_subype.link_doc_type)

	doc.append('tab_opcon', {
		'link_opcon_meta': meta.name,
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

	new_opcon: DC_Doc_Opcon_Meta = frappe.get_doc({
		'doctype': 'DC_Doc_Opcon_Meta',
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
		'attached_to_doctype': 'DC_Doc_Opcon_Meta',
		'attached_to_name': new_opcon.name,
		'attached_to_field': 'attached_file',
	})
	new_file.insert()

	add_existing_opcon(prod_id, misc={'label': new_opcon.name})

	return True


@frappe.whitelist()
def add_desdoc(prod_id, upload, temp_file):
	ds = frappe.parse_json(upload)

	if ds['label']:
		add_existing_desdoc(prod_id, ds)
	else:
		add_new_desdoc(prod_id, ds, temp_file)

	return 'success'


def add_existing_desdoc(prod_id, misc):
	doc: DC_PLC_Product_Summary = frappe.get_doc('DC_PLC_Product_Summary', prod_id)
	meta: DC_Doc_Desdoc_Meta = frappe.get_doc('DC_Doc_Desdoc_Meta', misc['label'])
	doc_subype = frappe.get_doc('DC_Doc_Document_Subtype', meta.link_subtype)
	doc_type = frappe.get_doc('DC_Doc_Document_Type', doc_subype.link_doc_type)

	doc.append('tab_desdoc', {
		'link_desdoc_meta': meta.name,
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

	new_desdoc: DC_Doc_Desdoc_Meta = frappe.get_doc({
		'doctype': 'DC_Doc_Desdoc_Meta',
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
		'attached_to_doctype': 'DC_Doc_Desdoc_Meta',
		'attached_to_name': new_desdoc.name,
		'attached_to_field': 'attached_file',
	})
	new_file.insert()

	add_existing_desdoc(prod_id, misc={'label': new_desdoc.name})

	return True
