# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals, division

from collections import defaultdict

import frappe
from frappe import _

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


@frappe.whitelist(allow_guest=True)
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


@frappe.whitelist(allow_guest=True)
def developer_query_with_empty_developer(doctype, txt, searchfield, start, page_len, filters):
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

    res = frappe.db.sql("""SELECT em.employee, em.employee_name
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
                         }, as_list=1)

    # FIXME HACK to handle empty developers in products case
    return [['HR-EMP-00094', '-']] + res


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
