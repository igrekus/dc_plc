import openpyxl
import frappe
import datetime

from six import BytesIO


class ExcelProductListExport:
	def __init__(self, headers, fields, data):
		self._headers = headers
		self._rows = [[data_object[f] for f in fields] for data_object in data]

	def serve(self):
		wb = openpyxl.Workbook()
		ws = wb.active

		self._append_header(ws)
		self._append_data(ws)

		xlsx_file = BytesIO()
		wb.save(xlsx_file)

		frappe.response['filename'] = self._generate_filename()
		frappe.response['filecontent'] = xlsx_file.getvalue()
		frappe.response['type'] = 'binary'

	def _append_header(self, sheet):
		header_cell = sheet['A1']
		for col, header in enumerate(['№'] + self._headers):
			header_cell.offset(0, 0 + col).value = header

	def _append_data(self, sheet):
		data_cell = sheet['A2']
		for row, row_data in enumerate(self._rows):
			for col, value in enumerate(row_data):
				data_cell.offset(0 + row, 0).value = row + 1
				data_cell.offset(0 + row, 1 + col).value = value

	def _generate_filename(self):
		return 'products_export_{}.xlsx'.format(datetime.date.today().isoformat())


def export_list_xlsx(headers, fields, data):
	export = ExcelProductListExport(headers, fields, data)
	export.serve()

