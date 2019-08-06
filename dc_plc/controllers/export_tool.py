import frappe
import ast


@frappe.whitelist(allow_guest=True)
def export_product_numbers(ids):
	"""
	Search for members of the developer group (GRP00002)
	:param doctype:
	:param txt:
	:param searchfield:
	:param start:
	:param page_len:
	:param filters:
	:return:
	"""

	db_name = frappe.conf.get("db_name")
	id_array = sorted(set(ast.literal_eval(ids)))
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
	:param doctype:
	:param txt:
	:param searchfield:
	:param start:
	:param page_len:
	:param filters:
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
