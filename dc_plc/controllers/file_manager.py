import frappe
import os
import six
from urllib.parse import quote


@frappe.whitelist()
def get_file_meta(doctype, docname, field_name):
	db_name = frappe.conf.get("db_name")

	sql = f"""
SELECT
	`f`.`name`
	, `f`.`file_name`
	, `f`.`file_url`
	, `f`.`creation`
FROM `{db_name}`.`tabFile` AS `f`
WHERE `f`.`attached_to_doctype` = %(doctype)s
AND `f`.`attached_to_name` = %(docname)s"""

	res = frappe.db.sql(
		query=sql + ';',
		values={
			'doctype': f'{doctype}',
			'docname': f'{docname}'
		},
		as_dict=1
	)

	return res[0] if res else {}


@frappe.whitelist()
def get_doc_meta(doctype, docname):
	db_name = frappe.conf.get("db_name")

	sql = f"""
SELECT `f`.`name`
, `f`.`file_name`
, `f`.`file_url`
, `f`.`creation`
, `t`.`title` AS `type`
FROM `{db_name}`.`tabFile` AS `f`
INNER JOIN `{db_name}`.`tabDC_Doc_Meta` AS `dm` ON `dm`.`name` = `f`.`attached_to_name`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Subtype` AS `st` ON `st`.`name` = `dm`.`link_subtype`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Type` AS `t` ON `t`.`name` = `st`.`link_doc_type`
WHERE `dm`.`name` = %(docname)s"""

	res = frappe.db.sql(
		query=sql + ';',
		values={
			'docname': f'{docname}'
		},
		as_dict=1
	)

	return res[0] if res else {}


@frappe.whitelist()
def serve_document(meta_id):
	# TODO refactor concrete doc serve functions
	db_name = frappe.conf.get("db_name")

	sql = f"""
	SELECT
	`m`.`title` AS `meta_title`
	, `m`.`attached_file`
	FROM `{db_name}`.`tabDC_Doc_Meta` AS `m`
	WHERE `m`.`name` = %(meta_id)s
	"""
	res = frappe.db.sql(
		query=sql + ';',
		values={
			'meta_id': f'{meta_id}'
		},
		as_list=1
	)

	target, source = res[0]
	serve_as_filename(source, target)


@frappe.whitelist()
def serve_as_filename(src_url, target_name):
	# TODO use config to get site path: filepath = frappe.utils.get_site_path(path)
	source = f'./site1.local/public{src_url}'
	with open(source, mode='rb') as f:
		frappe.response['filename'] = f"{quote(target_name)}"
		frappe.response['filecontent'] = six.BytesIO(f.read()).getvalue()
		frappe.response['type'] = 'binary'


@frappe.whitelist()
def datasheet_search_query(doctype, txt, searchfield, start, page_len, filters):
	"""
	:param doctype:
	:param txt:
	:param searchfield:
	:param start:
	:param page_len:
	:param filters:
	:return:
	"""

	db_name = frappe.conf.get("db_name")

	sql = f"""
SELECT
	`m`.`name`
	, `m`.`title`
FROM `{db_name}`.tabDC_Doc_Datasheet_Meta AS `m`
WHERE 
	(`m`.`name` LIKE %(search)s OR `m`.`title` LIKE %(search)s)
ORDER BY
	`m`.`name` ASC, `m`.`title` ASC"""

	res = frappe.db.sql(
		sql + ';',
		{
			'search': '%{}%'.format(txt)
		}
	)

	return res
