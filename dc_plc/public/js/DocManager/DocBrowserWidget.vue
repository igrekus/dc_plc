<template>
	<div>
		<el-button @click="onNewDocClicked">Новый документ</el-button>

		<el-dialog
				:visible.sync="dialogTableVisible"
				width="80%"
				:before-close="onBeforeClose">
			<template slot="title"><span class="el-dialog__title">{{ title }}</span></template>
			<doc-file-dialog
					ref="documentMetaDialog"
					v-bind:formData="formData"
					v-on:confirm="onConfirm"></doc-file-dialog>
		</el-dialog>

		<el-input
				placeholder="Фильтр списка докуметов..."
				v-model="filterText">
		</el-input>

		<el-table
				ref="tableDocs"
				:data="tableData"
				style="width: 100%"
				height="600"
				@cell-click="onCellClicked">
			<div slot="empty">
				Нет данных
			</div>
			<el-table-column type="expand">
				<template slot-scope="props">
					<p>Связан с изделиями:</p>
					<ul>
						<li v-for="link in props.row.prod_links">{{ link.ext_num }}</li>
					</ul>
				</template>
			</el-table-column>
			<el-table-column
					type="index">
			</el-table-column>
			<el-table-column
					prop="filename"
					label="Имя файла">
			</el-table-column>
			<el-table-column
					prop="subtype"
					label="Подтип"
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
					width="100" align="center">
				<template slot-scope="scope">
					<el-button
							size="small"
							type="primary"
							icon="el-icon-edit"
							plain
							@click="onRowEditClicked(scope.$index, scope.row)">
					</el-button>
				</template>
			</el-table-column>
		</el-table>
	</div>
</template>

<script>
	import DocFileDialog from './DocFileDialog.vue'

	export default {
		name: "DocBrowserWidget",
		data() {
			return {
				title: 'Новый документ',
				tableData: [],
				filterText: '',
				dialogTableVisible: false,
				formData: {
					id: null,
					name: '',
					type: '',
					subtype: '',
					tempFileName: '',
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
				this.title = 'Новый документ';
				this.formData = {
					id: null,
					name: '',
					type: 'DT001',
					subtype: 'DST002',
					tempFileName: '',
					note: '',
					optional: {
						num: '',
						int_num: '',
						date_approve: new Date().toISOString().slice(0, 10),
						date_archive: new Date().toISOString().slice(0, 10),
					},
					products: [],
				};
				this.dialogTableVisible = true;
			},

			editDocument(row_data) {
				this.title = 'Редактировать докумет';
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

			onCellClicked(row, column, cell, event) {
				if (cell.cellIndex === 6) return;
				if (!row.prod_links.length) {
					let me = this;
					frappe.call({
						method: "dc_plc.dc_documents.page.doc_manager.controller.get_doc_links",
						args: {
							id_: row.id,
							type_id: row.type_id,
						},
						callback: function (r) {
							row.prod_links = r.message;
						}
					});
				}
				this.$refs.tableDocs.toggleRowExpansion(row);
			},

			onRowEditClicked(index, row_data) {
				this.editDocument(row_data);
			},

			onNewDocClicked() {
				this.newDocument();
			},

			onConfirm(form) {
				this.dialogTableVisible = false;
				let me = this;
				// TODO select correct method on the backend
				const method  = this.formData.id ? 'update_document' : 'add_new_document';
				frappe.call({
					method: `dc_plc.dc_documents.page.doc_manager.controller.${method}`,
					args: {
						form_data: form,
					},
					callback: function (r) {
						me.$message.info(me.formData.id ? 'Документ обновлён' : 'Документ создан');
					}
				});
			},

			onBeforeClose(done) {
				this.$refs.documentMetaDialog.removeTempFiles();
				done();
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

<style>
	.el-table__row {
		height: 20px;
	}
</style>