import frappe

from dc_plc.controllers.productexporter import export_list_xlsx, export_cards_xlsx


@frappe.whitelist(allow_guest=True)
def export_product_numbers(ids):
	"""
	Search for members of the developer group (GRP00002)
	:param ids:
	:return:
	"""

	db_name = frappe.conf.get("db_name")
	id_array = sorted(set(frappe.parse_json(ids)))
	id_str = '"' + '","'.join(id_array) + '"'

	res = frappe.db.sql("""SELECT
	`p`.`ext_num`
	, `p`.`int_num`
	, `proj`.`title`
	FROM `{}`.tabDC_PLC_Product_Summary AS `p`
	INNER JOIN `{}`.tabDC_PLC_RND_Project as `proj` ON `p`.`link_rnd_project` = `proj`.`name`
	WHERE `p`.`name` IN ({})
	ORDER BY `p`.`name` ASC""".format(db_name, db_name, id_str))

	return [{
			'number': num + 1,
			'ext_num': row[0],
			'int_num': row[1],
			'rnd_proj': row[2]
		} for num, row in enumerate(res)]


@frappe.whitelist(allow_guest=True)
def export_product_search(query=''):
	"""
	Search for members of the developer group (GRP00002)
	:param query:
	:return:
	"""

	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql("""SELECT
	`p`.`name`
	, `p`.`ext_num`
	, `p`.`int_num`
	, `proj`.`title`
	FROM `{}`.tabDC_PLC_Product_Summary AS `p`
	INNER JOIN `{}`.tabDC_PLC_RND_Project as `proj` ON `p`.`link_rnd_project` = `proj`.`name`
	WHERE `p`.`ext_num` LIKE "%{}%"
		OR `p`.`int_num` LIKE "%{}%"
		OR `proj`.`title` LIKE "%{}%"
	ORDER BY `p`.`ext_num` ASC, `p`.`int_num` ASC
	LIMIT 10""".format(db_name, db_name, query, query, query))

	return [{
			'value': row[0],
			'ext_num': row[1],
			'int_num': row[2],
			'rnd_proj': row[3]
		} for row in res]


@frappe.whitelist(allow_guest=True)
def export_product_data(ids=""):
	"""
	Search for members of the developer group (GRP00002)
	:param ids:
	:return:
	"""

	db_name = frappe.conf.get("db_name")
	id_array = sorted(set(frappe.parse_json(ids)))
	id_str = '"' + '","'.join(id_array) + '"'

	sql = """SELECT
	`p`.`name` as `id`
	, `p`.`ext_num`
	, `p`.`int_num`
	, `status`.`title` AS `status`
	, `letter`.`title` AS `letter`
	, `type`.`title` AS `type`
	, `proj`.`title` AS `project`
	, `p`.`chip`
	, `p`.`asm_board`
	, `pak`.`title` AS `package`
	, `fun`.`title` AS `function`
	, `p`.`application`
	, `p`.`description`
	, `p`.`specs`
	, `p`.`analog`
	, `p`.`desdoc_num`
	, `p`.`opcon`
	, `p`.`process_map`
	, `p`.`report`
	, `p`.`datasheet`
	, `p`.`final_description`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Status` AS `status` ON `p`.`link_status` = `status`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Letter` AS `letter` ON `p`.`link_letter` = `letter`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFt JOIN
		`{}`.`tabDC_PLC_Package` AS `pak` ON `p`.`link_package` = `pak`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`
	WHERE `p`.`name` IN ({})
	ORDER BY `p`.`name` ASC""" \
		.format(db_name, db_name, db_name, db_name, db_name, db_name, db_name, id_str)

	res = frappe.db.sql(sql + ';')

	return [{
		'id': row[0],
		'value': row[0],
		'ext_num': row[1],
		'int_num': row[2],
		'status': row[3],
		'letter': row[4],
		'type': row[5],
		'rnd_proj': row[6],
		'chip': row[7],
		'asm_board': row[8],
		'package': row[9],
		'func': row[10],
		'application': row[11],
		'description': row[12],
		'specs': row[13],
		'analogs': row[14],
		'desdoc_num': row[15],
		'opcon_num': row[16],
		'procmap_num': row[17],
		'reports': row[18],
		'datasheet': row[19],
		'final_description': row[20]
	} for row in res]


@frappe.whitelist()
def export_list_excel(headers, fields, ids):
	return export_list_xlsx(
		frappe.parse_json(headers),
		frappe.parse_json(fields),
		export_product_data(ids)
	)

