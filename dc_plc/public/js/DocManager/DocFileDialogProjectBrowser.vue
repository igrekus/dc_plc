<template>
	<div>
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
					<div class="rnd_proj">ОКР: <span class="item-text">{{ item.rnd_proj }}</span></div>
				</div>
			</template>
		</el-autocomplete>
		<el-table
				ref="exportTable"
				v-bind:data="productsInfo"
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
	</div>
</template>

<script>
	export default {
		name: "DocFileDialogProjectBrowser",
		props: {
			value: Array,
		},
		data() {
			return {
				state: '',
				content: [],
			}
		},
		computed: {
			productsInfo: function () {
				if (!this.content.length) {
					return [];
				}
				let prod_data = [];
				frappe.call({
					method: "dc_plc.controllers.export_tool.export_product_numbers",
					args: {
						ids: this.content.sort(),
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
				if (this.content.indexOf(id) === -1) {
					let arr = [...this.content];
					arr.push(id);
					arr.sort();
					this.content = arr;
				}
				this.state = '';
			},
			handleDelete(row_index, row_object) {
				this.content.splice(row_index, 1);
			}
		},
		watch: {
			productsInfo(newVal, oldVal) {
				this.$emit('input', this.content);
			},
		},
		mounted() {
			this.content = [...this.value];
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