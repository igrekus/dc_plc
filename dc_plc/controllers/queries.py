# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe


# search for members of consultant group (GRP00000)
def consultant_query(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""SELECT em.employee, em.employee_name
        FROM tabEmployee as em
        INNER JOIN tabDC_Employees_in_Group as gp
        ON em.employee = gp.link_employee
        WHERE gp.parent = "GRP00000"
          AND em.status = 'Active'
          AND (em.name like %(search)s OR
               em.employee_name like %(search)s)
        ORDER BY
            em.employee_name, em.name""",
                         {
                             'search': '%{}%'.format(txt)
                         })

# search for members of the developer group (GRP00001)
def developer_query(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""SELECT em.employee, em.employee_name
        FROM tabEmployee as em
        INNER JOIN tabDC_Employees_in_Group as gp
        ON em.employee = gp.link_employee
        WHERE gp.parent = "GRP00001"
          AND status = 'Active'
          AND (em.name like %(search)s OR
               em.employee_name like %(search)s)
        ORDER BY
            em.employee_name, em.name""",
                         {
                             'search': '%{}%'.format(txt)
                         })

