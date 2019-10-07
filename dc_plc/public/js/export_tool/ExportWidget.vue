<template>
	<div>
		<el-row>
			<h3>Настройки печати</h3>
			<el-checkbox v-model="shouldExportList" label="Экспорт списка изделий"></el-checkbox>
			<el-checkbox v-model="shouldExportCards" label="Экспорт карточек изделий"></el-checkbox>
			<el-checkbox v-model="shouldExportDatasheets" label="Экспорт даташитов" disabled></el-checkbox>
			<br/>
			<el-button type="primary" size="small" v-on:click="onExportClicked" v-bind:disabled="canExport">Экспорт</el-button>
			<el-button type="primary" size="small" v-on:click="onPrintClicked" v-bind:disabled="canExport">Печать</el-button>
		</el-row>
		<el-row>
			<h3>Предварительный просмотр</h3>
			<el-checkbox-button size="mini" v-model="checkedAll" v-on:change="onAllChecked">
				Все
			</el-checkbox-button>
			<el-checkbox-group size="mini" v-model="checkedColumns" v-on:change="onColumnChecked">
				<el-checkbox-button v-for="col in columns" v-bind:label="col.propName">
					{{ col.label }}
				</el-checkbox-button>
			</el-checkbox-group>
		</el-row>
		<el-table
				ref="exportDataTable"
				v-bind:data="productData"
				style="width: 100%">
			<div slot="empty">
				Нет данных
			</div>
			<el-table-column v-for="col in columns"
							 v-if="col.visible"
							 :property="col.propName"
							 :label="col.label"
							 :width="col.width">
			</el-table-column>
		</el-table>
	</div>

</template>

<script>
	export default {
		name: "export-widget",
		props: {
			productIds: Array,
		},
		data: function () {
			return {
				columns: [
					{
						label: 'Отраслевой номер',
						propName: 'ext_num',
						width: 'auto',
						visible: false
					},
					{
						label: 'Внутренний номер',
						propName: 'int_num',
						width: 'auto',
						visible: false
					},
					{
						label: 'Развитие',
						propName: 'status',
						width: 'auto',
						visible: false
					},
					{
						label: 'Литерность',
						propName: 'letter',
						width: 'auto',
						visible: false
					},
					{
						label: 'Разработчик',
						propName: 'devs',
						width: 'auto',
						visible: false
					},
					{
						label: 'Консультант',
						propName: 'cons',
						width: 'auto',
						visible: false
					},
					{
						label: 'Тип',
						propName: 'type',
						width: 'auto',
						visible: false
					},
					{
						label: 'ОКР',
						propName: 'rnd_proj',
						width: 'auto',
						visible: false
					},
					{
						label: 'Кристалл',
						propName: 'chip',
						width: 'auto',
						visible: false
					},
					{
						label: 'Плата в сборке',
						propName: 'asm_board',
						width: 'auto',
						visible: false
					},
					{
						label: 'Корпус',
						propName: 'package',
						width: 'auto',
						visible: false
					},
					{
						label: 'Функция',
						propName: 'func',
						width: 'auto',
						visible: false
					},
					{
						label: 'Применение',
						propName: 'application',
						width: 'auto',
						visible: false
					},
					{
						label: 'Техническое описание',
						propName: 'description',
						width: 'auto',
						visible: false
					},
					{
						label: 'Параметры',
						propName: 'specs',
						width: 'auto',
						visible: false
					},
					{
						label: 'Аналоги',
						propName: 'analogs',
						width: 'auto',
						visible: false
					},
					{
						label: 'Номер КД',
						propName: 'desdoc_num',
						width: 'auto',
						visible: false
					},
					{
						label: 'Номер ТУ',
						propName: 'opcon_num',
						width: 'auto',
						visible: false
					},
					{
						label: 'Номер ТК',
						propName: 'procmap_num',
						width: 'auto',
						visible: false
					},
					{
						label: 'Отчёты',
						propName: 'reports',
						width: 'auto',
						visible: false
					},
					{
						label: 'Даташит',
						propName: 'datasheet',
						width: 'auto',
						visible: false
					},
					{
						label: 'Финальное описание',
						propName: 'final_description',
						width: 'auto',
						visible: false
					},
					{
						label: 'Примечание тех. специалиста',
						propName: 'tech_note',
						width: 'auto',
						visible: false
					},
					{
						label: 'Примечание экономиста',
						propName: 'economy_note',
						width: 'auto',
						visible: false
					},
				],
				checkedAll: false,
				checkedColumns: [],
				productData: [],
				shouldExportList: false,
				shouldExportCards: false,
				shouldExportDatasheets: false,
			}
		},
		computed: {
			canExport: function () {
				return !(this.shouldExportList || this.shouldExportCards || this.shouldExportDatasheets);
			}
		},
		methods: {
			onAllChecked: function () {
				let arr = [];
				this.columns.forEach(col => {
					col.visible = this.checkedAll;
					arr.push(col.propName);
				});
				this.checkedColumns = this.checkedAll ? arr : [];
			},
			onExportFlagToggled: function () {
				console.log('toggle');
			},
			onColumnChecked: function (cols) {
				// TODO simplify this mess
				this.columns.forEach(col => {
					col.visible = !!cols.find(el => {
						return el === col.propName;
					});
				})
			},
			onPrintClicked: function () {
				this.printProducts({
					list: this.shouldExportList,
					cards: this.shouldExportCards,
					datasheets: this.shouldExportDatasheets,
				});
			},
			onExportClicked: function () {
				this.exportProducts({
					list: this.shouldExportList,
					cards: this.shouldExportCards,
					datasheets: this.shouldExportDatasheets,
				});
			},
			exportProducts: function (exports) {
				const to_export = this.columns.filter(col => {
					return col.visible;
				});
				open_url_post('/api/method/dc_plc.controllers.export_tool.get_xlsx', {
					exports: exports,
					headers: to_export.map(col => {
						return col.label;
					}),
					fields: to_export.map(col => {
						return col.propName;
					}),
					ids: this.productIds,
				});
			},
			printProducts: function (exports) {
				const to_export = this.columns.filter(col => {
					return col.visible;
				});
				// open_url_post('/api/method/dc_plc.controllers.export_tool.get_pdf', {
				// 	exports: exports,
				// 	headers: to_export.map(col => {
				// 		return col.label;
				// 	}),
				// 	fields: to_export.map(col => {
				// 		return col.propName;
				// 	}),
				// 	ids: this.productIds,
				// }, true);
				frappe.call({
					method: 'dc_plc.controllers.export_tool.get_pdf',
					args: {
						exports: exports,
						headers: to_export.map(col => {
							return col.label;
						}),
						fields: to_export.map(col => {
							return col.propName;
						}),
						ids: this.productIds,
					},
					callback: r => {
						let w = window.open();
						if (!w) {
							frappe.msgprint(__("Please enable pop-ups in your browser"))
						}
						w.document.write(r.message);
						w.document.close();
					}
				});

			}
		},
		watch: {
			productIds: function (newVal, oldVal) {
				if (!this.productIds.length) {
					return [];
				}
				let prod_data = [];
				frappe.call({
					method: "dc_plc.controllers.export_tool.export_product_data",
					args: {
						ids: this.productIds,
					},
					async: false,
					callback: r => {
						prod_data = r.message;
					}
				});
				this.productData = prod_data;
			}
		},
		mounted: function () {
			// this.checkedColumns = this.columns.map(col => {
			// 	return col.propName;
			// });
			this.checkedAll = false;
		}
	}
</script>

<style scoped>

</style>