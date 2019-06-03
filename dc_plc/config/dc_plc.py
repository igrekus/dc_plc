# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from frappe import _
import frappe

def get_data():

    return [
        {
            "label": _("DC Product Info"),
            "icon": "octicon octicon-briefcase",
            "items": [
                {
                    "type": "report",
                    "name": "DC Product Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Full stats"),
                    "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                    # 			"type": 'link',
                    # 			"link": '#social/home',
                    # 			"color": '#FF4136',
                    # 			'standard': 1,
                    # 			'idx': 15,
                    # 			"description": "Build your profile and share posts with other users."
                    # 			"system_manager": 1,
                    # 					"hide_count": True
                },
                {
                    "type": "report",
                    "name": "DC Product RND Specialist Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("RND Spec query"),
                    # "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
                {
                    "type": "report",
                    "name": "DC Product Developer Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Developer query"),
                    # "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
                {
                    "type": "report",
                    "name": "DC Product Opcon Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Opcon spec query"),
                    # "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
                {
                    "type": "report",
                    "name": "DC Product Tech Writer Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Tech writer query"),
                    # "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
            ]
        },
        {
            "label": _("Product filters"),
            "icon": "octicon octicon-briefcase",
            "items": [
                {
                    "type": "report",
                    "name": "DC Product Filter RND Project",
                    "is_query_report": True,
                    "doctype": "DC_PLC_RND_Project",
                    "label": _("By RND project"),
                },
                {
                    "type": "report",
                    "name": "DC Product Filter Product Type",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Type",
                    "label": _("By type"),
                },
                {
                    "type": "report",
                    "name": "DC Product Filter Function",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Function",
                    "label": _("By function"),
                    # "onboard": 1,
                    # "dependencies": ["DC_PLC_Product_Summary"],
                    # "condition": getattr(frappe.local.conf, 'developer_mode', 0),
                },
                {
                    "type": "report",
                    "name": "DC Product Filter Package",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Package",
                    "label": _("By package"),
                },
                {
                    "type": "report",
                    "name": "DC Product Filter Model",
                    "is_query_report": True,
                    "label": _("By letter"),
                },
                {
                    "type": "report",
                    "name": "DC Product Filter Status",
                    "is_query_report": True,
                    "label": _("By status"),
                },
                # {
                #     "type": "page",
                #     "label": _("Activity"),
                #     "name": "activity",
                #     "description": _("Activity log of all users."),
                # },
            ]
        },
        {
            "label": _("Module settings"),
            "icon": "octicon octicon-briefcase",
            "items": [
                {
                    "type": "doctype",
                    "name": "DC_PLC_Product_Summary",
                    "label": _("DC Products"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_Package",
                    "label": _("Package type"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_Product_Function",
                    "label": _("Function"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_Product_Type",
                    "label": _("Product type"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_RND_Project",
                    "label": _("RND title"),
                },
                {
                    "type": "doctype",
                    "name": "DC_Employee_Group",
                    "label": _("Employee Group"),
                },
            ]
        },
    ]
