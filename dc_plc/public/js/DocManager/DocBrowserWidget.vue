<template>
	<div>
		<el-button @click="onNewDocClicked">Новый документ</el-button>

		<el-dialog title="Новый документ" :visible.sync="dialogTableVisible">
			<doc-file-dialog v-bind:formData="formData"></doc-file-dialog>
		</el-dialog>

		<el-input
				placeholder="Filter keyword"
				v-model="filterText">
		</el-input>

		<el-table
				:data="tableData"
				style="width: 100%"
				height="600"
				@row-click="onRowClicked">
			<div slot="empty">
				Нет данных
			</div>
			<el-table-column
					type="index">
			</el-table-column>
			<el-table-column
					prop="filename"
					label="Имя файла">
			</el-table-column>
			<el-table-column
					prop="subtype"
					label="Тип"
					width="150">
			</el-table-column>
			<el-table-column
					prop="int_num"
					label="Внутренний номер"
					width="150">
			</el-table-column>
			<el-table-column
					prop="ext_num"
					label="Внешний номер"
					width="150">
			</el-table-column>
			<el-table-column
					prop="prod_links"
					label="Используется в"
					width="150">
			</el-table-column>
		</el-table>
	</div>
</template>

<script>
	import DocFileDialog from './DocFileDialog.vue'
	let id = 1000;

	export default {
		name: "DocBrowserWidget",
		data() {
			return {
				tableData: [],
				filterText: '',
				dialogTableVisible: false,
				formData: {
					id: null,
					name: '',
					type: '',
					subtype: '',
					note: '',
					optional: {
						num: '',
						int_num: '',
						date_approve: null,
						date_archive: null,
					},
					products: [],
				}
			}
		},

		methods: {
			append(data) {
				const newChild = {id: id++, label: 'testtest', children: []};
				if (!data.children) {
					this.$set(data, 'children', []);
				}
				data.children.push(newChild);
			},

			remove(node, data) {
				const parent = node.parent;
				const children = parent.data.children || parent.data;
				const index = children.findIndex(d => d.id === data.id);
				children.splice(index, 1);
			},

			newDocument() {
				console.log('new doc');
				this.formData = {
					id: null,
					name: '',
					type: '',
					subtype: '',
					note: '',
					optional: {
						num: '',
						int_num: '',
						date_approve: null,
						date_archive: null,
					},
					products: [],
				};
				this.dialogTableVisible = true;
			},

			editDocument(row_data) {
				let me = this;
				frappe.call({
					method: "dc_plc.dc_documents.page.doc_manager.controller.get_doc_meta",
					args: {
						id_: row_data.id,
						type_id: row_data.type_id,
					},
					callback: function (r) {
						me.formData = r.message;
						me.dialogTableVisible = true;
					}
				});
			},

			onRowClicked(row_data, column, event) {
				this.editDocument(row_data);
			},

			onNewDocClicked() {
				this.newDocument();
			},
			updateTable(filters={}) {
				let me = this;
				frappe.call({
					method: "dc_plc.dc_documents.page.doc_manager.controller.get_document_list",
					args: {
						filters: filters,
					},
					callback: function (r) {
						me.tableData = r.message;
					}
				});
			},
		},
		mounted() {
			this.updateTable();
		},
		components: {
			DocFileDialog,
		},
	}
</script>

<style scoped>
	.el-table__row {
		height: 20px;
	}
</style>