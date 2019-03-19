from __future__ import unicode_literals
from frappe import _


def get_data():

    return [
        {
            "label": _("DC product tracking"),
            "icon": "octicon octicon-briefcase",
            "items": [
                {
                    "type": "report",
                    "name": "DC Product Stats",
                    "is_query_report": True,
                    "doctype": "DC_PLC_Product_Summary",
                    "label": _("Product Stats"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_Package",
                    "label": _("Package type"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_Product_Function",
                    "label": _("Product function"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_Product_Type",
                    "label": _("Product type"),
                },
                {
                    "type": "doctype",
                    "name": "DC_PLC_RND_Project",
                    "label": _("R&D project"),
                },
            ]
        },
        {
            "label": _("DC Staff"),
            "icon": "octicon octicon-briefcase",
            "items": [
                {
                    "type": "doctype",
                    "name": "DC_Employee_Group",
                    "label": _("Employees group"),
                },
            ]
        }
    ]
