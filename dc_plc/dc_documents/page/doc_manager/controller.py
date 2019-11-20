import frappe


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
ORDER BY `subtype` ASC
""")

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
def get_doc_meta(id_):
	db_name = frappe.conf.get("db_name")

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
, 'links'
FROM `{db_name}`.`tabDC_Doc_Meta` AS `m`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Subtype` AS `st` ON `m`.`link_subtype` = `st`.`name`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Type` AS `t` ON `t`.`name` = `st`.`link_doc_type`
WHERE `m`.`name` = '{id_}'
ORDER BY `subtype` ASC;""", as_dict=1)[0]

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
	}
