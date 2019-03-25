from __future__ import unicode_literals
from frappe import _
import frappe

def get_data():

    return [
        {
            "label": _("Статистика продукции НО-8"),
            "icon": "octicon octicon-briefcase",
            "items": [
                {
                    "type": "report",
                    "name": "DC Product Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Полная статистика"),
                    "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
                {
                    "type": "report",
                    "name": "DC Product RND Specialist Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Выборка для специалиста по ОКР"),
                    # "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
                {
                    "type": "report",
                    "name": "DC Product Developer Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Выборка для разработчика"),
                    # "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
                {
                    "type": "report",
                    "name": "DC Product Opcon Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Выборка для специалиста по ТУ"),
                    # "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
                {
                    "type": "report",
                    "name": "DC Product Tech Writer Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Выборка для технического писателя"),
                    # "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
                # {
                #     "type": "report",
                #     "name": "DC Product Stats",
                #     "is_query_report": True,
                #     "doctype": "DC_PLC_Product_Summary",
                #     "label": _("Product Tech Writer Stats"),
                #     # "onboard": 1,
                #     "dependencies": ["DC_PLC_Product_Summary"],
                #     # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                # },
            ]
        },
        {
            "label": _("Источники данных"),
            "icon": "octicon octicon-briefcase",
            "items": [
                {
                    "type": "doctype",
                    "name": "DC_PLC_Product_Summary",
                    "label": _("Продукция"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_Package",
                    "label": _("Тип корпуса"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_Product_Function",
                    "label": _("Функциональное назначение"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_Product_Type",
                    "label": _("Тип устройства"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_RND_Project",
                    "label": _("Наименование ОКР"),
                },
            ]
        },
        {
            "label": _("Данные о сотрудниках НО-8"),
            "icon": "octicon octicon-briefcase",
            "items": [
                {
                    "type": "doctype",
                    "name": "DC_Employee_Group",
                    "label": _("Группа сотрудников"),
                },
            ]
        }
    ]
