# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals, division

from collections import defaultdict

import frappe
from dc_plc.custom.utils import count_filled_fields


def consultant_query(doctype, txt, searchfield, start, page_len, filters):
    """
    Search members of consultant group (GRP00001)
    :param doctype:
    :param txt:
    :param searchfield:
    :param start:
    :param page_len:
    :param filters:
    :return:
    """

    db_name = frappe.conf.get("db_name")

    return frappe.db.sql("""SELECT em.employee, em.employee_name
        FROM  `{}`.tabEmployee as em
        INNER JOIN `{}`.tabDC_Employees_in_Group as gp
        ON em.employee = gp.link_employee
        WHERE gp.parent = "GRP00001"
          AND em.status = 'Active'
          AND (em.name like %(search)s OR
               em.employee_name like %(search)s)
        ORDER BY
            em.employee_name, em.name""".format(db_name, db_name),
                         {
                             'search': '%{}%'.format(txt)
                         })


def developer_query(doctype, txt, searchfield, start, page_len, filters):
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

    return frappe.db.sql("""SELECT em.employee, em.employee_name
        FROM `{}`.tabEmployee as em
        INNER JOIN `{}`.tabDC_Employees_in_Group as gp
        ON em.employee = gp.link_employee
        WHERE gp.parent = "GRP00002"
          AND status = 'Active'
          AND (em.name like %(search)s OR
               em.employee_name like %(search)s)
        ORDER BY
            em.employee_name, em.name""".format(db_name, db_name),
                         {
                             'search': '%{}%'.format(txt)
                         })


def developers_in_product():

    db_name = frappe.conf.get("db_name")

    return frappe.db.sql("""SELECT CONCAT(emp.last_name, " ", emp.first_name, " ", emp.middle_name) AS developers
FROM `{}`.`tabDC_PLC_Developers_in_Product` AS t
INNER JOIN `{}`.tabEmployee AS emp
ON t.link_employee = emp.employee;
""".format(db_name, db_name))


def consultants_in_product():

    db_name = frappe.conf.get("db_name")

    return frappe.db.sql("""SELECT CONCAT(emp.last_name, " ", emp.first_name, " ", emp.middle_name) AS consultants
    FROM `{}`.`tabDC_PLC_Consulants_in_Product` AS t
    INNER JOIN `{}`.tabEmployee AS emp
    ON t.link_employee = emp.employee;
    """.format(db_name, db_name))


def product_stats_full():

    db_name = frappe.conf.get("db_name")

    return frappe.db.sql("""SELECT
  p.name as `id`
     , p.ext_num
     , type.title
     , proj.title
     , "stub"
     , "stub"
     , p.chip
     , p.asm_board
     , pak.title
     , fun.title
     , p.application
     , p.description
     , p.specs
     , p.opcon
     , p.analog
     , p.report
     , p.datasheet
FROM `{}`.tabDC_PLC_Product_Summary AS p
INNER JOIN `{}`.tabDC_PLC_Product_Type AS type,
           `{}`.tabDC_PLC_RND_Project AS proj,
           `{}`.tabDC_PLC_Package AS pak,
           `{}`.tabDC_PLC_Product_Function AS fun;""".format(db_name, db_name, db_name, db_name, db_name), as_list=1)


@frappe.whitelist(allow_guest=True)
def role_completeness_stats():
    # TODO refactor this

    db_name = frappe.conf.get("db_name")

    res = frappe.db.sql("""SELECT 
       `p`.`sel_status`
     , COUNT(`cons`.`link_employee`) AS `con_num`
     , COUNT(`devs`.`link_employee`) AS `dev_num`    
     , `p`.`link_rnd_project`     
     , `p`.`link_type`
     , `p`.`sel_model`
     , `p`.`link_function`
     , `p`.`chip`
     , `p`.`asm_board`
     , `p`.`link_package`
     , `p`.`description`
     , `p`.`specs`
     , `p`.`report`
     , `p`.`analog`     
     , `p`.`ext_num`
     , `p`.`opcon`
     , `p`.`process_map`     
     , `p`.`application`
     , `p`.`datasheet`
     , `p`.`int_num`
     , `p`.`desdoc_num`
FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
LEFT JOIN `{}`.`tabDC_PLC_Consulants_in_Product` AS `cons` ON `cons`.parent = `p`.`name`
LEFT JOIN `{}`.`tabDC_PLC_Developers_in_Product` AS `devs` ON `devs`.parent = `p`.`name`
GROUP BY `p`.`name`;
""".format(db_name, db_name, db_name), as_list=1)

    total = [count_filled_fields(row, range(len(row))) for row in res]
    total = [int(round(row[0]/row[1], 2) * 100) for row in total]
    total = int(sum(total)/len(total))

    dept_head = [count_filled_fields(row, range(3)) for row in res]
    dept_head = [int(round(row[0]/row[1], 2) * 100) for row in dept_head]
    dept_head = int(sum(dept_head)/len(dept_head))

    rnd_spec = [count_filled_fields(row, [3]) for row in res]
    rnd_spec = [int(round(row[0]/row[1], 2) * 100) for row in rnd_spec]
    rnd_spec = int(sum(rnd_spec)/len(rnd_spec))

    developer = [count_filled_fields(row, range(4, 14)) for row in res]
    developer = [int(round(row[0]/row[1], 2) * 100) for row in developer]
    developer = int(sum(developer)/len(developer))

    opcon = [count_filled_fields(row, [14, 15]) for row in res]
    opcon = [int(round(row[0]/row[1], 2) * 100) for row in opcon]
    opcon = int(sum(opcon)/len(opcon))

    process = [count_filled_fields(row, [16]) for row in res]
    process = [int(round(row[0]/row[1], 2) * 100) for row in process]
    process = int(sum(process)/len(process))

    tech_writer = [count_filled_fields(row, [17, 18]) for row in res]
    tech_writer = [int(round(row[0]/row[1], 2) * 100) for row in tech_writer]
    tech_writer = int(sum(tech_writer)/len(tech_writer))

    desdoc = [count_filled_fields(row, [17, 18]) for row in res]
    desdoc = [int(round(row[0]/row[1], 2) * 100) for row in desdoc]
    desdoc = int(sum(desdoc)/len(desdoc))

    return [
        {"name": "Department head", "progress": dept_head},
        {"name": "RND specialist", "progress": rnd_spec},
        {"name": "Developer", "progress": developer},
        {"name": "Opcon specialist", "progress": opcon},
        {"name": "Process specialist", "progress": process},
        {"name": "Tech writer", "progress": tech_writer},
        {"name": "Desdoc specialist", "progress": desdoc},
        {"name": "Total", "progress": total}
    ]


@frappe.whitelist(allow_guest=True)
def developer_completeness_stats():
    # TODO refactor this

    db_name = frappe.conf.get("db_name")

    res = frappe.db.sql("""SELECT CONCAT(`emps`.last_name, ' ', `emps`.first_name, ' '     , `emps`.middle_name) AS `dev`
     , `devs`.`link_employee`
     , `p`.`link_type`
     , `p`.`sel_model`
     , `p`.`link_function`
     , `p`.`chip`
     , `p`.`asm_board`
     , `p`.`link_package`
     , `p`.`description`
     , `p`.`specs`
     , `p`.`report`
     , `p`.`analog`
FROM `{}`.tabDC_PLC_Product_Summary AS p
INNER JOIN `{}`.tabDC_PLC_Developers_in_Product AS `devs` ON `devs`.parent = `p`.`name`
INNER JOIN `{}`.tabEmployee AS `emps` ON `devs`.link_employee = `emps`.`name`
ORDER BY `dev` ASC;""".format(db_name, db_name, db_name))

    temp = defaultdict(list)
    for row in res:
        name, emp_id, *data = row
        temp[name].append(count_filled_fields(data, range(len(data))))

    output = dict()
    for name, stats in temp.items():
        s = [int(round(row[0] / row[1], 2) * 100) for row in stats]
        output[name] = int(sum(s) / len(s))

    return sorted([{'name': k, "progress": v} for k, v in output.items()], key=lambda e: e['name'])
