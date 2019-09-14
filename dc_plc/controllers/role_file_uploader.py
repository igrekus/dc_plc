import frappe


@frappe.whitelist()
def search_existing_datasheets(query):
	"""
	Search for existing datasheets
	:param query: str -- text search query
	:return: list -- list of {'value': '', 'label': ''} entries
	"""

	db_name = frappe.conf.get("db_name")

	res = frappe.db.sql(f"""
SELECT
	`m`.`name`
	, `m`.`title` AS `meta_title`
	, `m`.`note` AS `note`
	, `m`.`attached_file` AS `url`
FROM
	`{db_name}`.tabDC_Doc_Datasheet_Meta AS `m`
INNER JOIN
	`{db_name}`.tabDC_Doc_Document_Subtype AS `s` ON `m`.`link_subtype` = `s`.`name`
WHERE
	`s`.`name` = 'DST002'
AND
	`m`.`title` LIKE  %(search)s 
LIMIT 10;""", {
		'search': '%{}%'.format(query)
	})

	return [
		{
			'label': d[0],
			'value': d[1],
			'note': d[2],
			'file_url': d[3].replace('\n', '<br>')
		}
		for d in res
	]
