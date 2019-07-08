# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals, division

from collections import defaultdict
from operator import itemgetter

import frappe
from frappe import _

from dc_plc.custom.utils import count_filled_fields


@frappe.whitelist(allow_guest=True)
def role_completeness_stats():
    # TODO refactor this
    # TODO refactor hardcoded column indexes
    db_name = frappe.conf.get("db_name")

    res = frappe.db.sql("""SELECT 
       `p`.`link_status`
     , COUNT(`cons`.`link_employee`) AS `con_num`
     , COUNT(`devs`.`link_employee`) AS `dev_num`
     , `p`.`link_rnd_project`
     , `p`.`link_type`
     , `p`.`link_letter`
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
     , `p`.`rel_check_dept_head`
     , `p`.`rel_check_rnd_spec`
     , `p`.`rel_check_developer`
     , `p`.`rel_check_opcon`
     , `p`.`rel_check_procmap`
     , `p`.`rel_check_tech_writer`
     , `p`.`rel_check_desdoc`
FROM `{}`.`tabDC_PLC_Product_Summary` AS `p`
LEFT JOIN `{}`.`tabDC_PLC_Consulants_in_Product` AS `cons` ON `cons`.parent = `p`.`name`
LEFT JOIN `{}`.`tabDC_PLC_Developers_in_Product` AS `devs` ON `devs`.parent = `p`.`name`
GROUP BY `p`.`name`;
""".format(db_name, db_name, db_name), as_list=1)

    total = [count_filled_fields(row, range(len(row))) for row in res]
    total = [int(round(row[0]/row[1], 2) * 100) for row in total]
    total = int(sum(total)/len(total))

    dept_head = [count_filled_fields(row, [0, 1, 2]) for row in res]
    dept_head = [int(round(row[0]/row[1], 2) * 100) for row in dept_head]
    dept_head = int(sum(dept_head)/len(dept_head))

    rnd_spec = [count_filled_fields(row, [3]) for row in res]
    rnd_spec = [int(round(row[0]/row[1], 2) * 100) for row in rnd_spec]
    rnd_spec = int(sum(rnd_spec)/len(rnd_spec))

    developer = [count_filled_fields(row, [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]) for row in res]
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

    desdoc = [count_filled_fields(row, [19, 20]) for row in res]
    desdoc = [int(round(row[0]/row[1], 2) * 100) for row in desdoc]
    desdoc = int(sum(desdoc)/len(desdoc))

    rel_check_dept_head = round((sum([row[21] for row in res]) / len(res)) * 100)
    rel_check_rnd_spec = round((sum([row[22] for row in res]) / len(res)) * 100)
    rel_check_developer = round((sum([row[23] for row in res]) / len(res)) * 100)
    rel_check_opcon = round((sum([row[24] for row in res]) / len(res)) * 100)
    rel_check_procmap = round((sum([row[25] for row in res]) / len(res)) * 100)
    rel_check_tech_writer = round((sum([row[26] for row in res]) / len(res)) * 100)
    rel_check_desdoc = round((sum([row[27] for row in res]) / len(res)) * 100)

    host = frappe.utils.get_url()

    return [
        {
            "name": _("Dept head"),
            "progress": dept_head,
            "relevant": rel_check_dept_head,
            "url": "{}/desk#query-report/DC Product MMIC Dept Head Stats".format(host)
         },
        {
            "name": _("RnD spec"),
            "progress": rnd_spec,
            "relevant": rel_check_rnd_spec,
            "url": "{}/desk#query-report/DC Product RND Specialist Stats".format(host)
        },
        {
            "name": _("Developer"),
            "progress": developer,
            "relevant": rel_check_developer,
            "url": "{}/desk#query-report/DC Product Developer Stats".format(host)
        },
        {
            "name": _("Opcon spec"),
            "progress": opcon,
            "relevant": rel_check_opcon,
            "url": "{}/desk#query-report/DC Product Opcon Stats".format(host)
        },
        {
            "name": _("Procmap spec"),
            "progress": process,
            "relevant": rel_check_procmap,
            "url": "{}/desk#query-report/DC Product Procmap Stats".format(host)
        },
        {
            "name": _("Tech writer"),
            "progress": tech_writer,
            "relevant": rel_check_tech_writer,
            "url": "{}/desk#query-report/DC Product Tech Writer Stats".format(host)
        },
        {
            "name": _("Desdoc spec"),
            "progress": desdoc,
            "relevant": rel_check_desdoc,
            "url": "{}/desk#query-report/DC Product Desdoc Stats".format(host)
        },
        {
            "name": _("Total"),
            "progress": total,
            "relevant": sum([rel_check_dept_head, rel_check_rnd_spec, rel_check_developer,
                             rel_check_opcon, rel_check_procmap, rel_check_tech_writer, rel_check_desdoc]) / 7,
            "url": "{}/desk#query-report/DC%20Product%20Stats".format(host)
        }
    ]


@frappe.whitelist(allow_guest=True)
def developer_completeness_stats():
    # TODO refactor this

    db_name = frappe.conf.get("db_name")

    res = frappe.db.sql("""SELECT CONCAT(`emps`.last_name, ' ', `emps`.first_name, ' ', `emps`.middle_name) AS `dev`
     , `devs`.`link_employee`
     , `p`.`link_type`
     , `p`.`link_letter`
     , `p`.`link_function`
     , `p`.`chip`
     , `p`.`asm_board`
     , `p`.`link_package`
     , `p`.`description`
     , `p`.`specs`
     , `p`.`report`
     , `p`.`analog`
     , `p`.`rel_check_dept_head`
     , `p`.`rel_check_rnd_spec`
     , `p`.`rel_check_developer`
     , `p`.`rel_check_opcon`
     , `p`.`rel_check_procmap`
     , `p`.`rel_check_tech_writer`
     , `p`.`rel_check_desdoc`
FROM `{}`.tabDC_PLC_Product_Summary AS p
LEFT OUTER JOIN `{}`.tabDC_PLC_Developers_in_Product AS `devs` ON `devs`.parent = `p`.`name`
LEFT OUTER JOIN `{}`.tabEmployee AS `emps` ON `devs`.link_employee = `emps`.`name`
ORDER BY `dev` ASC;""".format(db_name, db_name, db_name))

    temp = defaultdict(list)
    ids = dict()
    for row in res:
        name = row[0] if row[0] else '--'
        emp_id = row[1]
        data = row[2:12]
        rel = row[13:]
        ids[name] = emp_id
        temp[name].append([count_filled_fields(data, range(len(data))), int(round(sum(rel) / 7 * 100))])

    output = dict()
    for name, data in temp.items():
        s_list = list()
        rel_list = list()
        for row, rel in data:
            s_list.append(int(round(row[0] / row[1], 2) * 100))
            rel_list.append(rel)
        output[name] = [int(sum(s_list) / len(s_list)), int(sum(rel_list) / len(rel_list))]

    # frappe.model.meta.trim_tables(doctype='DC_PLC_Product_Summary')

    host = frappe.utils.get_url()

    return sorted(
        [{
            'name': k,
            "progress": v[0],
            "relevant": v[1],
            "url": "{}/desk#query-report/DC%20Product%20Stats/Report?developer={}".format(host, ids[k])
        } for k, v in output.items()],
        key=itemgetter('name'))
