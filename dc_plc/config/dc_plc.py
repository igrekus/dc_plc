from __future__ import unicode_literals
from frappe import _
import frappe

def get_data():

    return [
        {
            "label": _("DC Product Stats"),
            "icon": "octicon octicon-briefcase",
            "items": [
                {
                    "type": "report",
                    "name": "DC Product Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Product Full Stats"),
                    "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
                {
                    "type": "report",
                    "name": "DC Product RND Specialist Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Product RND Specialist Stats"),
                    # "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
                {
                    "type": "report",
                    "name": "DC Product Developer Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Product Developer Stats"),
                    # "onboard": 1,
                    "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
                # {
                #     "type": "report",
                #     "name": "DC Product Stats",
                #     "is_query_report": True,
                #     "doctype": "DC_PLC_Product_Summary",
                #     "label": _("Product Developer Stats"),
                #     # "onboard": 1,
                #     "dependencies": ["DC_PLC_Product_Summary"],
                #     # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                # },
                # {
                #     "type": "report",
                #     "name": "DC Product Stats",
                #     "is_query_report": True,
                #     "doctype": "DC_PLC_Product_Summary",
                #     "label": _("Product Opcon Stats"),
                #     # "onboard": 1,
                #     "dependencies": ["DC_PLC_Product_Summary"],
                #     # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                # },
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
            "label": _("DC Product Data"),
            "icon": "octicon octicon-briefcase",
            "items": [
                {
                    "type": "doctype",
                    "name": "DC_PLC_Product_Summary",
                    "label": _("Products"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_Package",
                    "label": _("Package types"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_Product_Function",
                    "label": _("Functions"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_Product_Type",
                    "label": _("Product types"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_RND_Project",
                    "label": _("R&D projects"),
                },
            ]
        },
        {
            "label": _("DC Staff Data"),
            "icon": "octicon octicon-briefcase",
            "items": [
                {
                    "type": "doctype",
                    "name": "DC_Employee_Group",
                    "label": _("Employee group"),
                },
            ]
        }
    ]
