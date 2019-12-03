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
				v-model="search">
		</el-input>

		<el-table
				ref="tableDocs"
    			:data="filteredTableData" style="width: 100%"
				:default-sort = "{prop: 'subtype', order: 'ascending'}"
				height="600"
				@cell-click="onCellClicked"
				@expand-change="onExpandChanged">
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
					label="Имя файла"
					sortable>
			</el-table-column>
			<el-table-column
					prop="subtype"
					label="Подтип"
					width="160"
					sortable
					:filters="[
						{ text: 'Отчёт КД', value: 'Отчёт КД' },
						{ text: 'Комплект КД', value: 'Комплект КД' },
						{ text: 'Габаритный чертёж', value: 'Габаритный чертёж' },
						{ text: 'ТУ исполнения', value: 'ТУ исполнения' },
						{ text: 'Единые ТУ', value: 'Единые ТУ' },
						{ text: 'Базовые ТУ ', value: 'Базовые ТУ ' },
						{ text: 'Общий', value: 'Общий' },
						{ text: 'Отчёт разработчика', value: 'Отчёт разработчика' },
						{ text: 'Даташит', value: 'Даташит' }
					]"
					:filter-method="filterSubtype"
					filter-placement="bottom-start">
			</el-table-column>
			<el-table-column
					prop="int_num"
					label="Номер"
					width="160"
					sortable>
			</el-table-column>
			<el-table-column
					prop="ext_num"
					label="Внешний номер"
					width="160"
					sortable>
			</el-table-column>
			<el-table-column
					width="150" align="center">
				<template slot-scope="scope">
					<el-tooltip class="item" effect="dark" content="Редактировать" placement="left">
						<el-button
								size="mini"
								type="primary"
								icon="el-icon-edit"
								plain
								@click="onRowEditClicked(scope.$index, scope.row)">
						</el-button>
					</el-tooltip>
					<el-tooltip class="item" effect="dark" content="Скачать" placement="right">
						<el-button
								size="mini"
								type="success"
								icon="el-icon-download"
								plain
								@click="onRowDownloadClicked(scope.$index, scope.row)">
						</el-button>
					</el-tooltip>
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
				search: '',
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
		computed: {
			filteredTableData() {
				let filtered = this.tableData.filter(el => {
					const s = this.search.toLowerCase();
					return !this.search
						|| (el.filename !== null && el.filename.toLowerCase().includes(s))
						|| (el.subtype !== null && el.subtype.toLowerCase().includes(s))
						|| (el.int_num !== null && el.int_num.toLowerCase().includes(s))
						|| (el.ext_num !== null && el.ext_num.toLowerCase().includes(s))
				});
				return filtered;
			}
		},
		methods: {
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
						date_approve: new Date(),
						date_archive: new Date(),
					},
					products: [],
				};
				this.dialogTableVisible = true;
			},

			editDocument(row_data) {
				this.title = 'Редактировать документ';
				let me = this;
				frappe.call({
					method: "dc_plc.dc_documents.page.doc_manager.controller.get_doc_meta",
					args: {
						id_: row_data.id,
						type_id: row_data.type_id,
					},
					callback: function (r) {
						let form = r.message;
						form.optional.date_approve = new Date(r.message.optional.date_approve);
						form.optional.date_archive = new Date(r.message.optional.date_archive);
						me.formData = {...form};
						me.formData.optional = {...form.optional};
						me.dialogTableVisible = true;
					}
				});
			},

			onCellClicked(row, column, cell, event) {
				if (cell.cellIndex === 6)
					return;
				this.$refs.tableDocs.toggleRowExpansion(row);
			},

			onRowEditClicked(index, row_data) {
				this.editDocument(row_data);
			},

			onRowDownloadClicked(index, row_data) {
				this.serve_document(row_data.id);
			},

			onNewDocClicked() {
				this.newDocument();
			},

			onConfirm(form) {
				this.dialogTableVisible = false;
				let me = this;

				let date_approve = this.addHours(form.optional.date_approve, 4);
				let date_archive = this.addHours(form.optional.date_archive, 4);

				// TODO select correct method on the backend
				const method  = this.formData.id ? 'update_document' : 'add_new_document';
				form.optional.date_approve = date_approve;
				form.optional.date_archive = date_archive;
				frappe.call({
					method: `dc_plc.dc_documents.page.doc_manager.controller.${method}`,
					args: {
						form_data: form,
					},
					callback: function (r) {
						me.$message.info(me.formData.id ? 'Документ обновлён' : 'Документ создан');
						me.updateTable();
					}
				});
			},

			onBeforeClose(done) {
				this.$refs.documentMetaDialog.removeTempFiles();
				done();
			},

			onExpandChanged(row, rows) {
				if (rows.indexOf(row) !== 0) {
					return;
				}
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

			filterSubtype(value, row) {
				return row.subtype === value;
			},

			addHours(date, hours) {
				let d = new Date(date);
				d.setHours(d.getHours() + hours);
				return d;
			},

			serve_document(id) {
				open_url_post('/api/method/dc_plc.controllers.file_manager.serve_document', { meta_id: id }, false);
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