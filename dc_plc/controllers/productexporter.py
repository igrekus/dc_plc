# -*- coding: utf-8 -*-

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
		'ext_num': u'Отраслевой номер',
		'rnd_proj': u'ОКР',
		'int_num': u'Внутренний номер',
		'type': u'Тип',
		'func': u'Функция',
		'letter': 'uЛитерность',
		'opcon_num': u'Номер ТУ',
		'status': u'Развитие',
		'devs': u'Разработчик',
		'cons': u'Консультант',
		'chip': u'Кристалл',
		'package': u'Корпус',
		'desdoc_num': u'Номер КД',
		'asm_board': u'Плата в сборке',
		'procmap_num': u'Номер ТК',
	}
	large_fields = {
		'application': u'Применение',
		'analogs': u'Аналоги',
		'final_description': u'Финально описание',
		'description': u'Техническое описание',
		'specs': u'Параметры',
		'reports': u'Отчёты',
		'datasheet': u'Даташит',
	}

	def __init__(self, headers, fields, product_data):
		self._headers = headers
		self._fields = {f: h for f, h in zip(fields, headers)}
		self._data = {field: product_data[field] for field in fields}
		self._small_fields = [field for field in self.small_fields.keys() if field in self._fields]
		self._large_fields = [field for field in self.large_fields.keys() if field in self._fields]

	def _append_header(self, sheet):
		header_cell = sheet['A1']
		header_cell.value = 'Карточка изделия'

	def _append_small_fields(self, sheet):
		base_cell = sheet['A2']
		col = 0
		row = 0
		for field in self._small_fields:
			base_cell.offset(0 + row, 0 + col * 3).value = self._fields[field]
			base_cell.offset(0 + row, 1 + col * 3).value = self._data[field]
			col += 1
			if col > 1:
				col = 0
				row += 1

	def _append_large_fields(self, sheet):
		base_cell = sheet['A' + str(sheet.max_row + 2)]
		for row, field in enumerate(self._large_fields):
			base_cell.offset(0 + row, 0). value = self._fields[field]
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
