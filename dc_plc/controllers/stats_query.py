import frappe


def get_full_stats(filters):
	db_name = frappe.conf.get("db_name")

	sql = """SELECT
	`p`.`name` as `id`
	, `status`.`title` AS `status`
	, `p`.`ext_num`
	, `p`.`int_num`
	, `letter`.`title` AS `letter`
	, `type`.`title` AS `type`
	, `proj`.`title` AS `project`
	, "stub" AS `cons`
	, "stub" AS `devs`
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
	, `p`.`report`
	, `p`.`datasheet`
	, `p`.`rel_check_dept_head`
	, `p`.`rel_check_rnd_spec`
	, `p`.`rel_check_developer`
	, `p`.`rel_check_opcon`
	, `p`.`rel_check_procmap`
	, `p`.`rel_check_tech_writer`
	, `p`.`rel_check_desdoc`
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
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`""" \
		.format(db_name, db_name, db_name, db_name, db_name, db_name, db_name)

	if filters:
		proj = filters.get('link_rnd_project', '%')
		proj_clause = "(`proj`.`name` LIKE '%' OR `proj`.`name` IS NULL)" if proj == '%' else "`proj`.`name` LIKE '{}'".format(proj)

		type_ = filters.get('link_type', '%')
		type_clause = "(`type`.`name` LIKE '%' OR `type`.`name` IS NULL)" if type_ == '%' else "`type`.`name` LIKE '{}'".format(type_)

		letter = filters.get('link_letter', '%')
		model_clause = "(`p`.`link_letter` LIKE '%' OR `p`.link_letter IS NULL)" if letter == '%' else "`p`.`link_letter` LIKE '{}'".format(letter)

		func = filters.get('link_function', '%')
		func_clause = "(`fun`.`name` LIKE '%' OR `fun`.`name` IS NULL)" if func == '%' else "`fun`.`name` LIKE '{}'".format(func)

		status = filters.get('link_status', '%')
		status_clause = "(`p`.`link_status` LIKE '%' OR `p`.link_status IS NULL)" if status == '%' else "`p`.`link_status` LIKE '{}'".format(status)

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
	, `status`.`title` AS `status`
	, `proj`.`title` AS `project`
	, "stub" AS `cons`
	, "stub" AS `devs`
	, `fun`.`title` AS `function`
	, `p`.`description`
	, `p`.`ext_num`
	, `p`.`int_num` 
	, `p`.`rel_check_dept_head`
	, `p`.`rel_date_dept_head`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Status` AS `status` ON `p`.`link_status` = `status`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`""".format(db_name, db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)


def get_rnd_spec_stats(filters):
	db_name = frappe.conf.get("db_name")

	sql = """SELECT
	`p`.`name` AS `id`
	, `status`.`title` AS `status`
	, `proj`.`title` AS `project`
	, `letter`.`title` AS `letter`
	, `func`.`title` AS `function`
	, `p`.`ext_num`
	, `p`.`int_num`
	, `p`.`rel_check_rnd_spec`
	, `p`.`rel_date_rnd_spec`
	FROM `{}`.tabDC_PLC_Product_Summary AS p
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Status` AS `status` ON `p`.`link_status` = `status`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `func` ON `p`.`link_function` = `func`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Letter` AS `letter` ON `p`.`link_letter` = `letter`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`;""".format(db_name, db_name, db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)


def get_developer_stats(filters):
	db_name = frappe.conf.get("db_name")

	sql = """SELECT
	`p`.`name` as `id`
	, `proj`.`title` AS `project`
	, `type`.`title` AS `type`
	, `letter`.`title` AS `letter`
	, `fun`.`title` AS `function`
	, `p`.`chip`
	, `p`.`asm_board`
	, `pak`.`title` AS `package`
	, `p`.`description`
	, `p`.`specs`
	, `p`.`report`
	, `p`.`analog`
	, `p`.`ext_num`
	, `p`.`int_num`
	, `p`.`rel_check_developer`
	, `p`.`rel_date_developer`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Letter` AS `letter` ON `p`.`link_letter` = `letter`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Package` AS `pak` ON `p`.`link_package` = `pak`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`;""".format(db_name, db_name, db_name, db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)


def get_opcon_stats(filters):
	db_name = frappe.conf.get("db_name")

	sql = """SELECT
	`p`.`name` as `id`
	, `proj`.`title` AS `project`
	, `type`.`title` AS `type`
	, `letter`.`title` AS `letter`
	, `fun`.`title` AS `function`
	, `p`.`ext_num`
	, `p`.`opcon`
	, `p`.`int_num`
	, `p`.`rel_check_opcon`
	, `p`.`rel_date_opcon`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Letter` AS `letter` ON `p`.`link_letter` = `letter`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Package` AS `pak` ON `p`.`link_package` = `pak`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`;""".format(db_name, db_name, db_name, db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)


def get_procmap_stats(filters):
	db_name = frappe.conf.get("db_name")

	sql = """SELECT
	`p`.`name` as `id`
	, `proj`.`title` AS `project`
	, `fun`.`title` AS `function`
	, `p`.`ext_num`
	, `p`.`process_map`
	, `p`.`opcon`
	, `p`.`int_num`
	, `p`.`rel_check_procmap`
	, `p`.`rel_date_procmap`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.link_rnd_project = `proj`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`;""".format(db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)


def get_tech_writer_stats(filters):
	db_name = frappe.conf.get("db_name")

	sql = """SELECT
	`p`.`name` AS `id`
	, `fun`.`title` AS `function`
	, `pack`.`title` AS `package`
	, `p`.`description`
	, `p`.`specs`
	, `p`.`report`
	, `p`.`analog`
	, `p`.`ext_num`
	, `p`.`int_num`
	, `p`.`application`
	, `p`.`datasheet`
	, `p`.`rel_check_tech_writer`
	, `p`.`rel_date_tech_writer`
	FROM `{}`.tabDC_PLC_Product_Summary AS p
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`
	LEFt JOIN
		`{}`.`tabDC_PLC_Package` AS `pack` ON `p`.`link_package` = `pack`.`name`;""".format(db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)


def get_desdoc_stats(filters):
	db_name = frappe.conf.get("db_name")

	sql = """SELECT
	`p`.`name` AS `id`
	, `proj`.`title` AS `porject`
	, `type`.`title` AS `type`
	, `fun`.`title` AS `function`
	, `p`.`ext_num`
	, `p`.`opcon`
	, `p`.`int_num`
	, `p`.`desdoc_num`
	, `p`.`rel_check_desdoc`
	, `p`.`rel_date_desdoc`
	FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
	LEFT JOIN
		`{}`.`tabDC_PLC_RND_Project` AS `proj` ON `p`.`link_rnd_project` = `proj`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Type` AS `type` ON `p`.`link_type` = `type`.`name`
	LEFT JOIN
		`{}`.`tabDC_PLC_Product_Function` AS `fun` ON `p`.`link_function` = `fun`.`name`;""".format(db_name, db_name, db_name, db_name)

	return frappe.db.sql(sql + ";", as_list=1)

