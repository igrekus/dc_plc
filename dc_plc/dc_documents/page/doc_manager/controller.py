import frappe


@frappe.whitelist()
def get_document_list(filters=None):
	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(f'''SELECT `m`.`name`
, `m`.`title`
, `st`.`title`
, `p`.`int_num`
, `p`.`ext_num`
, 'links'
FROM `{db_name}`.`tabDC_Doc_Datasheet_Meta` AS `m`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Subtype` AS `st` ON `m`.`link_subtype` = `st`.`name`
INNER JOIN `{db_name}`.`tabDC_Doc_Datasheets_in_Datasheet_List` AS `dsl` ON `m`.`name` = `dsl`.`link_datasheet_meta`
INNEr JOIN `{db_name}`.`tabDC_PLC_Product_Summary` AS `p` ON `dsl`.`parent` = `p`.`name`
UNION
SELECT `m`.`name`
, `m`.`title`
, `st`.`title`
, `p`.`int_num`
, `p`.`ext_num`
, 'links'
FROM `{db_name}`.`tabDC_Doc_Desdoc_Meta` AS `m`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Subtype` AS `st` ON `m`.`link_subtype` = `st`.`name`
INNER JOIN `{db_name}`.`tabDC_Doc_Desdoc_in_Desdoc_List` AS `dsl` ON `m`.`name` = `dsl`.`link_desdoc_meta`
INNEr JOIN `{db_name}`.`tabDC_PLC_Product_Summary` AS `p` ON `dsl`.`parent` = `p`.`name`
UNION
SELECT `m`.`name`
, `m`.`title`
, `st`.`title`
, `p`.`int_num`
, `p`.`ext_num`
, 'links'
FROM `{db_name}`.`tabDC_Doc_Misc_Meta` AS `m`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Subtype` AS `st` ON `m`.`link_subtype` = `st`.`name`
INNER JOIN `{db_name}`.`tabDC_Doc_Misc_in_Misc_List` AS `dsl` ON `m`.`name` = `dsl`.`link_misc_meta`
INNEr JOIN `{db_name}`.`tabDC_PLC_Product_Summary` AS `p` ON `dsl`.`parent` = `p`.`name`
UNION
SELECT `m`.`name`
, `m`.`title`
, `st`.`title`
, `p`.`int_num`
, `p`.`ext_num`
, 'links'
FROM `{db_name}`.`tabDC_Doc_Opcon_Meta` AS `m`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Subtype` AS `st` ON `m`.`link_subtype` = `st`.`name`
INNER JOIN `{db_name}`.`tabDC_Doc_Opcon_in_Opcon_List` AS `dsl` ON `m`.`name` = `dsl`.`link_opcon_meta`
INNEr JOIN `{db_name}`.`tabDC_PLC_Product_Summary` AS `p` ON `dsl`.`parent` = `p`.`name`
UNION
SELECT `m`.`name`
, `m`.`title`
, `st`.`title`
, `p`.`int_num`
, `p`.`ext_num`
, 'links'
FROM `{db_name}`.`tabDC_Doc_Dev_Report_Meta` AS `m`
INNER JOIN `{db_name}`.`tabDC_Doc_Document_Subtype` AS `st` ON `m`.`link_subtype` = `st`.`name`
INNER JOIN `{db_name}`.`tabDC_Doc_Dev_Report_in_Dev_Report_List` AS `dsl` ON `m`.`name` = `dsl`.`link_dev_report_meta`
INNEr JOIN `{db_name}`.`tabDC_PLC_Product_Summary` AS `p` ON `dsl`.`parent` = `p`.`name`''')

	return [{
		'id': row[0],
		'filename': row[1],
		'subtype': row[2],
		'int_num': row[3],
		'ext_num': row[4],
		'prod_links': row[5],
	} for row in res]
