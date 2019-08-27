import frappe


@frappe.whitelist()
def get_datasheet_meta(meta_id):
	db_name = frappe.conf.get("db_name")

	sql = f"""
SELECT
	`m`.`name` 
	, `m`.`title` AS `meta_title`
	, `t`.`title` AS `type_title`
FROM `{db_name}`.tabDC_Doc_Datasheet_Meta AS `m`
INNER JOIN  `{db_name}`.tabDC_Doc_Document_Type AS `t`
ON `m`.`link_doc_type` = `t`.`name`
WHERE `m`.`name` = %(meta_id)s
"""
	res = frappe.db.sql(
		query=sql + ';',
		values={
			'meta_id': f'{meta_id}'
		},
		as_dict=1
	)

	return res[0]


@frappe.whitelist()
def get_file_meta(doctype, docname, field_name):
	db_name = frappe.conf.get("db_name")

	sql = f"""
SELECT
	`f`.`name`
	, `f`.`file_name`
	, `f`.`file_url`
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

