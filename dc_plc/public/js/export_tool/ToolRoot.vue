<template>
	<div>
		<el-row>
			<el-table
					ref="exportTable"
					v-bind:data="productsToExport"
					style="width: 100%">
				<div slot="empty">
					Нет данных
				</div>
				<el-table-column property="number" label="№" width="40"></el-table-column>
				<el-table-column property="ext_num" label="Внешний номер" width="200"></el-table-column>
				<el-table-column property="int_num" label="Внутрений нормер" width="200"></el-table-column>
				<el-table-column property="rnd_proj" label="ОКР" width="300"></el-table-column>
				<el-table-column align="center" width="80">
					<template slot-scope="scope">
						<el-button
								size="mini"
								type="danger"
								icon="el-icon-delete"
								plain
								v-on:click="handleDelete(scope.$index, scope.row)">
						</el-button>
					</template>
				</el-table-column>
			</el-table>
			<div style="margin-top: 20px">
				<el-autocomplete
						placeholder="Поиск..."
						v-model="state"
						popper-class="product-autocomplete"
						v-bind:fetch-suggestions="querySearchAsync"
						v-on:select="handleAutocompleteSelect"
						v-bind:trigger-on-focus="false">
					<template slot-scope="{ item }">
						<div class="suggestion-item">
							<div class="ext_num">Внеш.: <span class="item-text">{{ item.ext_num }}</span></div>
							<div class="int_num">Внут.: <span class="item-text">{{ item.int_num }}</span></div>
						</div>
					</template>
				</el-autocomplete>
			</div>
		</el-row>
		<!--<el-divider/>-->
		<el-row>
			<export-widget v-bind:productIds="product_ids"></export-widget>
		</el-row>
	</div>
</template>

<script>
	import ExportWidget from './ExportWidget.vue'

	export default {
		name: "ToolRoot",
		data() {
			return {
				product_ids: [],
				state: '',
			}
		},
		computed: {
			productsToExport: function () {
				if (!this.product_ids.length) {
					return [];
				}
				let prod_data = [];
				frappe.call({
					method: "dc_plc.controllers.export_tool.export_product_numbers",
					args: {
						ids: this.product_ids.sort(),
					},
					async: false,
					callback: r => {
						prod_data = r.message;
					}
				});
				return prod_data;
			}
		},
		methods: {
			querySearchAsync(queryString, cb) {
				frappe.call({
					method: "dc_plc.controllers.export_tool.export_product_search",
					args: {
						query: queryString,
					},
					callback: r => {
						cb(r.message);
					}
				});
			},
			handleAutocompleteSelect(item) {
				let id = this.state;
				if (this.product_ids.indexOf(id) === -1) {
					let arr = [...this.product_ids];
					arr.push(id);
					arr.sort();
					this.product_ids = arr;
				}
				this.state = '';
			},
			handleDelete(row_index, row_object) {
				this.product_ids.splice(row_index, 1);
			}
		},
		components: {
			ExportWidget,
		}
	}
</script>

<style>
	.product-autocomplete li {
		line-height: normal;
		padding: 7px;
	}

	li {
		border-bottom-width: 1px;
		border-bottom-style: solid;
		border-bottom-color: #e1e1e1;
	}

	li .ext_num {
		width: 95%;
		font-size: 14px;
	}

	li .int_num {
		width: 95%;
		font-size: 14px;
	}

	li .item-text {
		float: right
	}
</style>