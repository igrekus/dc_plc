# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "dc_plc"
app_title = "DC PLC"
app_publisher = "igrekus"
app_description = "App for managing life cycle of the product of Design center."
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "igrekus@example.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/dc_plc/css/dc_plc.css"
# app_include_js = [
#     # "assets/dc_plc/js/views/productsummaryview.js",
#     "assets/dc_plc/js/dc_plc.js",
#     "assets/dc_plc/js/export_tool/export_tool.js"
# ]
app_include_js = "/assets/js/dc_plc.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/dc_plc/css/dc_plc.css"
# web_include_js = "/assets/dc_plc/js/dc_plc.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"dc_plc_product_summary": "dc_plc_product_summary_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "dc_plc.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "dc_plc.install.before_install"
# after_install = "dc_plc.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dc_plc.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"dc_plc.tasks.all"
# 	],
# 	"daily": [
# 		"dc_plc.tasks.daily"
# 	],
# 	"hourly": [
# 		"dc_plc.tasks.hourly"
# 	],
# 	"weekly": [
# 		"dc_plc.tasks.weekly"
# 	]
# 	"monthly": [
# 		"dc_plc.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "dc_plc.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dc_plc.event.get_events"
# }

