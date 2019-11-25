<template>
	<div>
		<el-form :model="form" :label-position="labelPosition" @submit.native.prevent label-width="150px">
			<el-form-item label="Название файла">
				<el-input v-model="form.name" autocomplete="off" />
			</el-form-item>
			<el-form-item v-if="!form.id" label="Новый файл">
				<el-upload
						drag
						action="api/method/dc_plc.controllers.role_file_uploader.upload_file"
						:limit="1"
						:before-upload="beforeUpload"
						:on-remove="handleRemove"
						:on-exceed="handleExceed"
						:on-success="handleSuccess"
						:http-request="handleUploadRequest"
						:file-list="fileList">
					<i class="el-icon-upload"></i>
					<div class="el-upload__text"><em>Перетащите</em> файл или <em>нажмите</em> мышкой</div>
				</el-upload>
			</el-form-item>
			<el-form-item label="Тип файла">
				<el-select v-model="form.type" placeholder="Выберите тип документа">
					<el-option v-for="type in types" :label="type.label" :value="type.value" :key="type.value"></el-option>
				</el-select>
			</el-form-item>
			<el-form-item label="Подтип файла">
				<el-select v-model="form.subtype" placeholder="Выберите подтип документа">
					<el-option v-for="sub in subtypes" :label="sub.label" :value="sub.value" :key="sub.value"></el-option>
				</el-select>
			</el-form-item>
			<el-form-item label="Комментарий">
				<el-input v-model="form.note" type="textarea" autosize />
			</el-form-item>
			<div v-if="isExtendedForm">
				<el-form-item label="Внутренний номер">
					<el-input v-model="form.optional.int_num" />
				</el-form-item>
				<el-form-item label="Номер">
					<el-input v-model="form.optional.num" />
				</el-form-item>
				<el-form-item v-if="form.type === 'DT004'" label="Дата утверждения">
					<el-date-picker v-model="form.optional.date_approve" type="date" prefix-icon="lol" />
				</el-form-item>
				<el-form-item label="Дата сдачи в архив">
					<el-date-picker v-model="form.optional.date_archive" type="date" prefix-icon="lol" />
				</el-form-item>
			</div>
			<el-form-item label="Связанные изделия"></el-form-item>
			<doc-file-dialog-project-browser v-model="form.products"></doc-file-dialog-project-browser>
		</el-form>
		<el-divider></el-divider>
		<span slot="footer" class="dialog-footer">
			<el-button type="primary" @click="confirm" :disabled="isSaveDisabled">Сохранить</el-button>
		</span>
	</div>
</template>

<script>
	import DocFileDialogProjectBrowser from './DocFileDialogProductBrowser.vue'

	export default {
		name: 'DocFileDialog',
		props: ['formData'],
		data() {
			return {
				allowedFileSize: 50,
				fileList: [],
				labelPosition: 'left',
				form: {
					id: null,
					name: '',
					type: '',
					subtype: '',
					note: 'note',
					currentUpload: '',
					optional: {
						num: '',
						int_num: '',
						date_approve: null,
						date_archive: null,
					},
					products: [],
				},
				// TODO get type-subtype info from the backend
				types: [
					{ label: 'Тех. писатель', value: 'DT001'},
					{ label: 'Разработчик', value: 'DT002'},
					{ label: 'Общий', value: 'DT003'},
					{ label: 'ТУ', value: 'DT004'},
					{ label: 'КД', value: 'DT005'},
				],
				typeSubtypeMap: {
					'DT001': [ { label: 'Даташит', value: 'DST002'} ],
					'DT002': [ { label: 'Отчёт разработчика', value: 'DST003'} ],
					'DT003': [ { label: 'Общий', value: 'DST004'} ],
					'DT004': [
						{ label: 'Базовые ТУ', value: 'DST005'},
						{ label: 'Единыые ТУ', value: 'DST006'},
						{ label: 'ТУ исполнения', value: 'DST007'},
					],
					'DT005': [
						{ label: 'Габаритный чертёж', value: 'DST008'},
						{ label: 'Комплект КД', value: 'DST009'},
						{ label: 'Отчёт КД', value: 'DST010'},
					],
				}
			}
		},
		computed: {
			subtypes() {
				if (!this.typeSubtypeMap[this.form.type])
					return [];
				let newSubs = [...this.typeSubtypeMap[this.form.type]];
				this.form.subtype = this.form.subtype ? this.form.subtype : '';
				return newSubs;
			},
			isExtendedForm() {
				return this.form.type === 'DT004' || this.form.type === 'DT005';
			},
			isSaveDisabled() {
				// TODO only disable save on missing uploaded file on a new file record
				return !this.form.id;
			}
		},
		methods: {
			confirm() {
				this.$emit('confirm', this.form);
			},
			beforeUpload(file) {
				const { size } = file;
				const isAllowedSize = (size / 1024 / 1024) < this.allowedFileSize;
				if (!isAllowedSize) {
					this.$message.warning(`Размер файла не должен превышать ${this.allowedFileSize} Мб`);
				}
				return isAllowedSize;
			},
			handleRemove(file, fileList) {
				self = this;
				frappe.call({
					method: "dc_plc.controllers.role_file_uploader.remove_temp_file",
					args: {
						filename: this.tempFileName,
					},
					callback: function () {
						self.form.fileName = null;
						self.form.currentUpload = null;
					}
				});
			},
			handleExceed(files, fileList) {
				this.$message.warning(`За один раз можно загрузить только один файл`);
			},
			handleSuccess(response, file) {
				return;

				// TODO rewrite for new uploader
				this.tempFileName = JSON.parse(response).message;
				this.fileName = file.name;

				this.currentUpload = {
					label: null,
					value: file.name,
					file_url: `./site1.local/public/files/${this.fileType}/`,
					note: this.note,
					subtype: this.selectedSubtype,
					opconNum: this.opconNum,
					opconIntNum: this.opconIntNum,
					dateApproval: this.dateApproval,
					dateArchive: this.dateArchive,
				};

				// TODO hack to indicate upload complete
				// const child_index = !!this.subtypeMethod ? 8 : 2;
				this.$children[2].$children[0].uploadFiles[0].status = 'success';
				this.isUploading = false;
			},
			handleUploadRequest(param) {
				return;
				this.isUploading = true;
				let url = "api/method/dc_plc.controllers.role_file_uploader.upload_file";
				let file = param.file;

				let form = new FormData();
				form.append("file", file);
				form.append("filename", file.name);
				form.append("fileType", this.fileType);

				let xhr = new XMLHttpRequest();

				xhr.open("POST", url, true);
				xhr.setRequestHeader('Accept', 'application/json');
				xhr.setRequestHeader('X-Frappe-CSRF-Token', frappe.csrf_token);

				if (xhr.upload) {
					xhr.upload.onprogress = function progress(e) {
						if (e.total > 0) {
							e.percent = e.loaded / e.total * 100;
						}
						param.onProgress(e);
					};
				}

				let self = this;
				xhr.onload = function () {
					self.handleSuccess(xhr.response, file);
				};
				xhr.send(form);
			},
		},
		watch: {
			formData(n, o) {
				this.form = {...n};
			}
		},
		mounted: function () {
			this.form = {...this.formData};
		},
		components: {
			DocFileDialogProjectBrowser,
		}
	}
</script>

<style>
	input[type="file"] {
		display: none;
	}

	.el-form-item {
		margin-bottom: 5px;
	}
</style>
