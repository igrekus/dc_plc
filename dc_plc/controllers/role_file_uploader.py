import frappe
from frappe.handler import is_whitelisted


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

	uploaded_file_name = './site1.local/temp/upload-' + frappe.generate_hash('', 10) + '.dat'
	with open(uploaded_file_name, 'wb') as f:
		f.write(content)

	return True
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
