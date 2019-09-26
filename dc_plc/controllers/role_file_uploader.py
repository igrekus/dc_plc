import contextlib
import frappe
import os
import shutil

from frappe.core.doctype.file.file import File
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
SELECT
	`m`.`name`
	, `m`.`title` AS `meta_title`
	, `m`.`note` AS `note`
	, `m`.`attached_file` AS `url`
FROM
	`{db_name}`.tabDC_Doc_Datasheet_Meta AS `m`
INNER JOIN
	`{db_name}`.tabDC_Doc_Document_Subtype AS `s` ON `m`.`link_subtype` = `s`.`name`
WHERE
	`s`.`name` = 'DST002'
AND
	`m`.`title` LIKE  %(search)s 
LIMIT 10;""", {
		'search': '%{}%'.format(query)
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
def upload_file(*args, **kwargs):

	files = frappe.request.files
	if 'file' in files:
		file = files['file']
		content = file.stream.read()
		filename = file.filename

	uploaded_file_name = './site1.local/temp/datasheet-' + frappe.generate_hash('', 10) + '.dat'
	with open(uploaded_file_name, 'wb') as f:
		f.write(content)

	return uploaded_file_name
	files = frappe.request.files
	is_private = frappe.form_dict.is_private
	doctype = frappe.form_dict.doctype
	docname = frappe.form_dict.docname
	fieldname = frappe.form_dict.fieldname
	file_url = frappe.form_dict.file_url
	folder = frappe.form_dict.folder or 'Home'
	method = frappe.form_dict.method
	content = None
	filename = None

	if 'file' in files:
		file = files['file']
		content = file.stream.read()
		filename = file.filename

	frappe.local.uploaded_file = content
	frappe.local.uploaded_filename = filename

	if frappe.session.user == 'Guest':
		import mimetypes
		filetype = mimetypes.guess_type(filename)[0]
		if filetype not in ['image/png', 'image/jpeg', 'application/pdf']:
			frappe.throw("You can only upload JPG, PNG or PDF files.")

	if method:
		method = frappe.get_attr(method)
		is_whitelisted(method)
		return method()
	else:
		ret = frappe.get_doc({
			"doctype": "File",
			"attached_to_doctype": doctype,
			"attached_to_name": docname,
			"attached_to_field": fieldname,
			"folder": folder,
			"file_name": filename,
			"file_url": file_url,
			"is_private": 0,
			"content": content
		})
		ret.save(ignore_permissions=True)
		return ret


@frappe.whitelist()
def remove_temp_file(filename):
	with contextlib.suppress(FileNotFoundError):
		os.remove(filename)
	return 'success'


@frappe.whitelist()
def add_datasheet(prod_id, datasheet, temp_file):
	ds = frappe.parse_json(datasheet)

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
	stored_url = target_file[20:]

	shutil.move(temp_file, target_file)
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
