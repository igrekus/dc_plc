import frappe


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

	return res[0]

