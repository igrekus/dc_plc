from __future__ import unicode_literals

import openpyxl
import frappe
import datetime
import zipfile
import os

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


class ExcelProductCardExport:
	small_fields = {
		'ext_num': 'Отраслевой номер',
		'rnd_proj': 'ОКР',
		'int_num': 'Внутренний номер',
		'type': 'Тип',
		'func': 'Функция',
		'letter': 'Литерность',
		'opcon_num': 'Номер ТУ',
		'status': 'Развитие',
		'devs': 'Разработчик',
		'cons': 'Консультант',
		'chip': 'Кристалл',
		'package': 'Корпус',
		'desdoc_num': 'Номер КД',
		'asm_board': 'Плата в сборке',
		'procmap_num': 'Номер ТК',
	}
	large_fields = {
		'application': 'Применение',
		'analogs': 'Аналоги',
		'final_description': 'Финально описание',
		'description': 'Техническое описание',
		'specs': 'Параметры',
		'reports': 'Отчёты',
		'datasheet': 'Даташит',
	}

	def __init__(self, headers, fields, product_data):
		self._headers = headers
		self._fields = fields
		self._data = {field: product_data[field] for field in fields}
		self._small_fields = [field for field in self.small_fields.keys() if field in fields]
		self._large_fields = [field for field in self.large_fields.keys() if field in fields]

	def _append_header(self, sheet):
		header_cell = sheet['A1']
		header_cell.value = 'Карточка изделия'

	def _append_small_fields(self, sheet):
		base_cell = sheet['A2']
		col = 0
		row = 0
		for field in self._small_fields:
			base_cell.offset(0 + row, 0 + col * 3).value = self.small_fields[field]
			base_cell.offset(0 + row, 1 + col * 3).value = self._data[field]
			col += 1
			if col > 1:
				col = 0
				row += 1

	def _append_large_fields(self, sheet):
		base_cell = sheet['A' + str(sheet.max_row + 2)]
		for row, field in enumerate(self._large_fields):
			base_cell.offset(0 + row, 0). value = self.large_fields[field]
			base_cell.offset(0 + row, 1). value = self._data[field]

	@property
	def filename(self):
		return '{}-({})-{}.xlsx'.format(
			self._data.get('int_num', '-'),
			self._data.get('ext_num', '-'),
			datetime.date.today().isoformat()
		)

	@property
	def as_bytes(self):
		wb = openpyxl.Workbook()
		ws = wb.active

		self._append_header(ws)
		self._append_small_fields(ws)
		self._append_large_fields(ws)

		xlsx_file = BytesIO()
		wb.save(xlsx_file)

		return xlsx_file.getvalue()


def export_cards_xlsx(headers, fields, data):
	zipname = './site1.local/public/files/outzip-' + frappe.generate_hash('', 10) + '.zip'
	with zipfile.ZipFile(zipname, 'w') as outzip:
		for prod in data:
			export = ExcelProductCardExport(headers, fields, prod)
			outzip.writestr(export.filename, export.as_bytes)

	with open(zipname, mode='rb') as f:
		frappe.response['filename'] = 'product_cards.zip'
		frappe.response['filecontent'] = BytesIO(f.read()).getvalue()
		frappe.response['type'] = 'binary'

	os.remove(zipname)
