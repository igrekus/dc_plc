import openpyxl
import frappe


class ExcelProductExport:
	def __init__(self, headers, fields, data):
		self._headers = headers
		self._rows = [[data_object[f] for f in fields] for data_object in data]

	def save(self):
		wb = openpyxl.Workbook()
		ws = wb.active

		self._append_header(ws)
		self._append_data(ws)

		wb.save('./site1.local/public/files/test.xlsx')
		return True

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


def export_xlsx(headers, fields, data):
	frappe.msgprint(str(fields))
	export = ExcelProductExport(headers, fields, data)
	return export.save()
