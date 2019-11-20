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
def get_doc_meta(id_, type_id):
	db_name = frappe.conf.get("db_name")

	table = {
		'DT001': 'tabDC_Doc_Datasheets_in_Datasheet_List',
		'DT002': 'tabDC_Doc_Dev_Report_in_Dev_Report_List',
		'DT003': 'tabDC_Doc_Misc_in_Misc_List',
		'DT004': 'tabDC_Doc_Opcon_in_Opcon_List',
		'DT005': 'tabDC_Doc_Desdoc_in_Desdoc_List',
	}[type_id]

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

