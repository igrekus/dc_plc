# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe


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
    
    return frappe.db.sql("""SELECT em.employee, em.employee_name
        FROM  `_1bd3e0294da19198`.tabEmployee as em
        INNER JOIN `_1bd3e0294da19198`.tabDC_Employees_in_Group as gp
        ON em.employee = gp.link_employee
        WHERE gp.parent = "GRP00001"
          AND em.status = 'Active'
          AND (em.name like %(search)s OR
               em.employee_name like %(search)s)
        ORDER BY
            em.employee_name, em.name""",
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
    return frappe.db.sql("""SELECT em.employee, em.employee_name
        FROM `_1bd3e0294da19198`.tabEmployee as em
        INNER JOIN `_1bd3e0294da19198`.tabDC_Employees_in_Group as gp
        ON em.employee = gp.link_employee
        WHERE gp.parent = "GRP00002"
          AND status = 'Active'
          AND (em.name like %(search)s OR
               em.employee_name like %(search)s)
        ORDER BY
            em.employee_name, em.name""",
                         {
                             'search': '%{}%'.format(txt)
                         })


def developers_in_product():
    return frappe.db.sql("""SELECT CONCAT(emp.last_name, " ", emp.first_name, " ", emp.middle_name) AS developers
FROM `_1bd3e0294da19198`.`tabDC_PLC_Developers_in_Product` AS t
INNER JOIN `_1bd3e0294da19198`.tabEmployee AS emp
ON t.link_employee = emp.employee;
""")


def consultants_in_product():
    return frappe.db.sql("""SELECT CONCAT(emp.last_name, " ", emp.first_name, " ", emp.middle_name) AS consultants
    FROM `_1bd3e0294da19198`.`tabDC_PLC_Consulants_in_Product` AS t
    INNER JOIN `_1bd3e0294da19198`.tabEmployee AS emp
    ON t.link_employee = emp.employee;
    """)


def product_stats_full():
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
FROM `_1bd3e0294da19198`.tabDC_PLC_Product_Summary AS p
INNER JOIN `_1bd3e0294da19198`.tabDC_PLC_Product_Type AS type,
           `_1bd3e0294da19198`.tabDC_PLC_RND_Project AS proj,
           `_1bd3e0294da19198`.tabDC_PLC_Package AS pak,
           `_1bd3e0294da19198`.tabDC_PLC_Product_Function AS fun;""", as_list=1)
