<template>
	<div>
		<h3>Предварительный просмотр</h3>
		<el-row>
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
						label: 'Внешний номер',
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
						label: 'Статус',
						propName: 'status',
						width: 'auto',
						visible: true
					},
					{
						label: 'Литера',
						propName: 'letter',
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
						label: 'Описание',
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
				checkedColumns: []
			}
		},
		computed: {
			productData: function () {
				if (!this.productIds.length) {
					return [];
				}
				return [
					{
						ext_num: 'external_numbrer',
						int_num: 'int_numbor',
						status: 'stutussss',
						letter: 'bukovka',
						type: 'tip4ik',
						rnd_proj: 'projetto',
						chip: 'kristallllll',
						asm_board: 'asmblr',
						package: 'upakovo4ka',
						func: 'fonkshon',
						application: 'prolojuha',
						description: 'opesuha',
						specs: 'ttX',
						analogs: 'spizjeno!',
						desdoc_num: 'ka de',
						opcon_num: 'te uu',
						procmap_num: 'technologyia',
						reports: 'et4eteg',
						datasheet: 'data shit lolol',
						final_description: 'final epta'
					}
				]
			},
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