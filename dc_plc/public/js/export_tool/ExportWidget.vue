<template>
	<div>
		<el-row>
			<h3>Настройки печати</h3>
			<el-checkbox v-model="shouldExportList" label="Экспорт списка изделий"></el-checkbox>
			<el-checkbox v-model="shouldExportCards" label="Экспорт карточек изделий"></el-checkbox>
			<el-checkbox v-model="ShouldExportDatasheets" label="Экспорт даташитов" disabled></el-checkbox>
			<br/>
			<el-button type="primary" size="small" v-on:click="onExportClicked">Экспорт</el-button>
			<el-button type="primary" size="small" v-on:click="onPrintClicked" disabled>Печать</el-button>
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
						visible: true
					},
					{
						label: 'Внутренний номер',
						propName: 'int_num',
						width: 'auto',
						visible: true
					},
					{
						label: 'Развитие',
						propName: 'status',
						width: 'auto',
						visible: true
					},
					{
						label: 'Литерность',
						propName: 'letter',
						width: 'auto',
						visible: true
					},
					{
						label: 'Разработчик',
						propName: 'devs',
						width: 'auto',
						visible: true
					},
					{
						label: 'Консультант',
						propName: 'cons`',
						width: 'auto',
						visible: true
					},
					{
						label: 'Тип',
						propName: 'type',
						width: 'auto',
						visible: true
					},
					{
						label: 'ОКР',
						propName: 'rnd_proj',
						width: 'auto',
						visible: true
					},
					{
						label: 'Кристалл',
						propName: 'chip',
						width: 'auto',
						visible: true
					},
					{
						label: 'Плата в сборке',
						propName: 'asm_board',
						width: 'auto',
						visible: true
					},
					{
						label: 'Корпус',
						propName: 'package',
						width: 'auto',
						visible: true
					},
					{
						label: 'Функция',
						propName: 'func',
						width: 'auto',
						visible: true
					},
					{
						label: 'Применение',
						propName: 'application',
						width: 'auto',
						visible: true
					},
					{
						label: 'Техническое описание',
						propName: 'description',
						width: 'auto',
						visible: true
					},
					{
						label: 'Параметры',
						propName: 'specs',
						width: 'auto',
						visible: true
					},
					{
						label: 'Аналоги',
						propName: 'analogs',
						width: 'auto',
						visible: true
					},
					{
						label: 'Номер КД',
						propName: 'desdoc_num',
						width: 'auto',
						visible: true
					},
					{
						label: 'Номер ТУ',
						propName: 'opcon_num',
						width: 'auto',
						visible: true
					},
					{
						label: 'Номер ТК',
						propName: 'procmap_num',
						width: 'auto',
						visible: true
					},
					{
						label: 'Отчёты',
						propName: 'reports',
						width: 'auto',
						visible: true
					},
					{
						label: 'Даташит',
						propName: 'datasheet',
						width: 'auto',
						visible: true
					},
					{
						label: 'Финальное описание',
						propName: 'final_description',
						width: 'auto',
						visible: true
					},
				],
				checkedAll: false,
				checkedColumns: [],
				productData: [],
				shouldExportList: false,
				shouldExportCards: true,
				ShouldExportDatasheets: false,
			}
		},
		computed: {
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
			onColumnChecked: function (cols) {
				// TODO simplify this mess
				this.columns.forEach(col => {
					col.visible = !!cols.find(el => {
						return el === col.propName;
					});
				})
			},
			onPrintClicked: function () {
				console.log('print config:', this.shouldExportList, this.shouldExportCards, this.ShouldExportDatasheets);
			},
			onExportClicked: function () {
				if (this.shouldExportList) {
					this.exportProductList();
				}
				if (this.shouldExportCards) {
					this.exportProductCards();
				}
			},
			exportHelper: function (method) {
				let to_export = this.columns.filter(col => {
					return col.visible;
				});
				open_url_post(method, {
					headers: to_export.map(col => {
						return col.label;
					}),
					fields: to_export.map(col => {
						return col.propName;
					}),
					ids: this.productIds,
				});
			},
			exportProductList: function () {
				this.exportHelper("/api/method/dc_plc.controllers.export_tool.export_list_excel");
			},
			exportProductCards: function () {
				// this.exportHelper("/api/method/dc_plc.controllers.export_tool.export_cards_excel");

				let to_export = this.columns.filter(col => {
					return col.visible;
				});
				frappe.call({
					method: "dc_plc.controllers.export_tool.export_cards_excel",
					args: {
						headers: to_export.map(col => {
							return col.label;
						}),
						fields: to_export.map(col => {
							return col.propName;
						}),
						ids: this.productIds,
					},
					async: false,
					callback: r => {
						console.log('cards');
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
			this.checkedColumns = this.columns.map(col => {
				return col.propName;
			});
			this.checkedAll = true;
		}
	}
</script>

<style scoped>

</style>