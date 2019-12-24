import frappe

from dc_plc.controllers.productexporter import export_xlsx, export_pdf


@frappe.whitelist(allow_guest=True)
def export_product_numbers(ids):
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
	LIMIT 100""".format(db_name, db_name, query, query, query))

	return [{
			'value': row[0],
			'ext_num': row[1],
			'int_num': row[2],
			'rnd_proj': row[3]
		} for row in res]


@frappe.whitelist(allow_guest=True)
def export_product_data(ids=""):
	db_name = frappe.conf.get("db_name")
	id_array = sorted(set(frappe.parse_json(ids)))
	id_str = '"' + '","'.join(id_array) + '"'

	sql = """SELECT
	`p`.`name` as `id`
	, `p`.`ext_num`
	, `p`.`int_num`
	, CONCAT(`mil`.`index`, '.', `stg`.`index`, '.', `stp`.`index`, ' ', `stp`.`title`) AS `status`
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
	, GROUP_CONCAT(`con`.`full_name`) AS `devs`
	, GROUP_CONCAT(`dev`.`full_name`) AS `cons`
	, `p`.`tech_note`
	, `p`.`economy_note`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
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
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Step` AS `stp` ON `stp`.`name` = `p`.`link_step`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Stage` AS `stg` ON `stg`.`name` = `stp`.`link_stage`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Milestone` AS `mil` ON `mil`.`name` = `stg`.`link_milestone`
	LEFT OUTER JOIN
		`{}`.`tabDC_PLC_Developers_in_Product` AS `dev` ON `p`.`name` = `dev`.`parent`
	LEFT OUTER JOIN
		`{}`.`tabDC_PLC_Consulants_in_Product` AS `con` ON `p`.`name` = `con`.`parent`
	WHERE `p`.`name` IN ({})
	GROUP BY `p`.`name`
	ORDER BY `p`.`name` ASC""" \
		.format(db_name, db_name, db_name, db_name, db_name, db_name, db_name, db_name, db_name, db_name, db_name, id_str)

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
		'final_description': row[20],
		'devs': row[21],
		'cons': row[22],
		'tech_note': row[23],
		'economy_note': row[24]
	} for row in res]


@frappe.whitelist()
def get_xlsx(exports, headers, fields, ids):
	return export_xlsx(
		frappe.parse_json(exports),
		frappe.parse_json(headers),
		frappe.parse_json(fields),
		export_product_data(ids)
	)


@frappe.whitelist()
def get_pdf(exports, headers, fields, ids):
	return export_pdf(
		frappe.parse_json(exports),
		frappe.parse_json(headers),
		frappe.parse_json(fields),
		export_product_data(ids)
	)
