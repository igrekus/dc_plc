import frappe


def get_full_stats(filters):
	db_name = frappe.conf.get("db_name")

	sql = """SELECT
	`p`.`name` as `id`
	, `p`.`sel_status`
	, `p`.`ext_num`
	, `p`.`int_num`
	, `p`.`sel_model`
	, `type`.`title`
	, `proj`.`title`
	, "stub"
	, "stub"
	, `p`.`chip`
	, `p`.`asm_board`
	, `pak`.`title`
	, `fun`.`title`
	, `p`.`application`
	, `p`.`description`
	, `p`.`specs`
	, `p`.`analog`
	, `p`.`desdoc_num`
	, `p`.`opcon`
	, `p`.`report`
	, `p`.`datasheet`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFt JOIN
		`{}`.`tabDC_PLC_Package` AS `pak` ON `p`.`link_package` = `pak`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`""" \
		.format(db_name, db_name, db_name, db_name, db_name)

	if filters:
		proj = filters.get('link_rnd_project', '%')
		proj_clause = "(`proj`.`name` LIKE '%' OR `proj`.`name` IS NULL)" if proj == '%' else "`proj`.`name` LIKE '{}'".format(proj)

		type_ = filters.get('link_type', '%')
		type_clause = "(`type`.`name` LIKE '%' OR `type`.`name` IS NULL)" if type_ == '%' else "`type`.`name` LIKE '{}'".format(type_)

		model = filters.get('sel_model', '%')
		model_clause = "(`p`.`sel_model` LIKE '%' OR `p`.sel_model IS NULL)" if model == '%' else "`p`.`sel_model` LIKE '{}'".format(model)

		func = filters.get('link_function', '%')
		func_clause = "(`fun`.`name` LIKE '%' OR `fun`.`name` IS NULL)" if func == '%' else "`fun`.`name` LIKE '{}'".format(func)

		status = filters.get('sel_status', '%')
		status_clause = "(`p`.`sel_status` LIKE '%' OR `p`.sel_status IS NULL)" if status == '%' else "`p`.`sel_status` LIKE '{}'".format(status)

		pack = filters.get('link_package', '%')
		pack_clause = "(`pak`.`name` LIKE '%' OR `pak`.`name` IS NULL)" if pack == '%' else "`pak`.`name` LIKE '{}'".format(pack)

		sql += """
	WHERE
	{}
	AND
	{}
	AND
	{}
	AND
	{}
	AND
	{}
	AND
	{} 
	""".format(proj_clause, type_clause, model_clause, func_clause, status_clause, pack_clause)

	return frappe.db.sql(sql + ';', as_list=1)


def get_developers_for_product():
	db_name = frappe.conf.get("db_name")
	sql = """SELECT t.parent,
GROUP_CONCAT(CONCAT(emp.last_name, " ", emp.first_name, " ", emp.middle_name)) AS developers
FROM `{}`.`tabDC_PLC_Developers_in_Product` AS t
INNER JOIN `{}`.`tabEmployee` AS emp
ON t.link_employee = emp.employee
GROUP BY t.parent;""".format(db_name, db_name)
	return {res[0]: res[1] for res in frappe.db.sql(sql, as_list=1)}


def get_consultants_for_product():
	db_name = frappe.conf.get("db_name")
	sql = """SELECT t.parent,
GROUP_CONCAT(CONCAT(emp.last_name, " ", emp.first_name, " ", emp.middle_name)) AS developers
FROM `{}`.tabDC_PLC_Consulants_in_Product AS t
INNER JOIN `{}`.`tabEmployee` AS emp
ON t.link_employee = emp.employee
GROUP BY t.parent;""".format(db_name, db_name)
	return {res[0]: res[1] for res in frappe.db.sql(sql, as_list=1)}


def get_dept_head_stats(filters):
	db_name = frappe.conf.get("db_name")

	sql = """SELECT
	`p`.`name` as `id`
	, `p`.`sel_status`
	, `proj`.`title`
	, "stub"
	, "stub"
	, `fun`.`title`
	, `p`.`description`
	, `p`.`ext_num`
	, `p`.`int_num` 
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`""".format(db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)


def get_rnd_spec_stats(filters):
	db_name = frappe.conf.get("db_name")

	sql = """SELECT
	`p`.`name` as `id`
	, `p`.`sel_status`
	, `proj`.`title`
	, `p`.`sel_model`
	, `func`.`title`
	, `p`.`ext_num`
	, `p`.`int_num`
	FROM `{}`.tabDC_PLC_Product_Summary AS p
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `func` ON `p`.`link_function` = `func`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`;""".format(db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)


def get_developer_stats(filters):
	db_name = frappe.conf.get("db_name")

	sql = """SELECT
	`p`.`name` as `id`
	, `proj`.`title`
	, `type`.`title`
	, `p`.`sel_model`
	, `fun`.`title`
	, `p`.`chip`
	, `p`.`asm_board`
	, `pak`.`title`
	, `p`.`description`
	, `p`.`specs`
	, `p`.`report`
	, `p`.`analog`
	, `p`.`ext_num`
	, `p`.`int_num`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Package` AS `pak` ON `p`.`link_package` = `pak`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`;""".format(db_name, db_name, db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)
