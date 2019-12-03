# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():

	# add 'Analytics' role
	allowed_roles = ['System Manager', 'Administrator']
	user_roles = frappe.get_roles(frappe.session.user)
	is_allowed = bool(set(user_roles).intersection(set(allowed_roles)))

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
					"name": "DC Product MMIC Dept Head Stats",
					"is_query_report": True,
					"doctype": "DC_PLC_Product_Summary",
					"label": _("Department head query"),
				},
				{
					"type": "report",
					"name": "DC Product RND Specialist Stats",
					"is_query_report": True,
					"doctype": "DC_PLC_Product_Summary",
					"label": _("RnD spec query"),
				},
				{
					"type": "report",
					"name": "DC Product Developer Stats",
					"is_query_report": True,
					"doctype": "DC_PLC_Product_Summary",
					"label": _("Developer query"),
				},
				{
					"type": "report",
					"name": "DC Product Opcon Stats",
					"is_query_report": True,
					"doctype": "DC_PLC_Product_Summary",
					"label": _("Opcon spec query"),
				},
				{
					"type": "report",
					"name": "DC Product Procmap Stats",
					"is_query_report": True,
					"doctype": "DC_PLC_Product_Summary",
					"label": _("Process spec query"),
				},
				{
					"type": "report",
					"name": "DC Product Desdoc Stats",
					"is_query_report": True,
					"doctype": "DC_PLC_Product_Summary",
					"label": _("Design doc spec query"),
				},
				{
					"type": "report",
					"name": "DC Product Tech Writer Stats",
					"is_query_report": True,
					"doctype": "DC_PLC_Product_Summary",
					"label": _("Tech writer query"),
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
					"name": "DC_PLC_Product_Function_Group",
					"label": _("Function group"),
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
					"name": "DC_PLC_Product_Status",
					"label": _("Status"),
				},
				{
					"type": "doctype",
					"name": "DC_PLC_Product_Letter",
					"label": _("Letter"),
				},
				{
					"type": "doctype",
					"name": "DC_Employee_Group",
					"label": _("Employee Group"),
				},
			],
			"condition": is_allowed,
		},
		{
			"label": _("Statistics"),
			"icon": "octicon octicon-briefcase",
			"items": [
				{
					"type": "page",
					"label": _("Product dashboard"),
					"name": "dc_product_dashboard",
					"description": _("Totals for DC Products"),
					"onboard": 1
				},
				{
					"type": "page",
					"label": _("Export tool"),
					"name": "dc_product_export",
					"description": _("Export DC product data"),
					"onboard": 1
				},
				{
					"type": "page",
					"label": _("Document manager"),
					"name": "doc_manager",
					"description": _("Manage Design Center documents"),
					"onboard": 1
				},
			],
			"condition": is_allowed
		},
		{
			"label": _("Statistics"),
			"icon": "octicon octicon-briefcase",
			"items": [
				{
					"type": "page",
					"label": _("Product dashboard"),
					"name": "dc_product_dashboard",
					"description": _("Totals for DC Products"),
					"onboard": 1
				},
				{
					"type": "page",
					"label": _("Export tool"),
					"name": "dc_product_export",
					"description": _("Export DC product data"),
					"onboard": 1
				},
			],
			"condition": not is_allowed
		}
	]
