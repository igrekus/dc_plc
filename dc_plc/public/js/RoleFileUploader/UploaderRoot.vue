<template>
	<div>
		<el-row>
			<el-switch
					v-model="uploadNew"
					inactive-color="#13ce66"
					inactive-text="Выбрать существующий"
					active-color="#409EFF"
					active-text="Загрузить новый"
					@change="handleAttachModeToggle">
			</el-switch>
		</el-row>
		<div v-if="uploadNew">
			<el-row>
				<el-input
						placeholder="Имя файла"
						v-model="fileName" />
			</el-row>
			<el-row>
				<el-input
						type="textarea"
						autosize
						placeholder="Комментарий..."
						v-model="note" />
			</el-row>
			<el-row>
				<el-upload
						class="upload-demo"
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
					<div class="el-upload__text">Для за грузки, перетащите файл <em>нажмите мышкой</em></div>
					<div class="el-upload__tip" slot="tip">PDF размером меньше 10 Мб</div>
				</el-upload>
			</el-row>
		</div>
		<div v-else>
			<el-row>
				<el-autocomplete
						placeholder="Поиск..."
						v-model="state"
						popper-class="product-autocomplete"
						v-bind:fetch-suggestions="querySearchAsync"
						v-on:select="handleAutocompleteSelect"
						v-bind:trigger-on-focus="true">
					<!--<template slot-scope="{ item }">-->
						<!--<div class="suggestion-item">-->
							<!--<div class="ext_num">Внеш.: <span class="item-text">{{ item.ext_num }}</span></div>-->
							<!--<div class="int_num">Внут.: <span class="item-text">{{ item.int_num }}</span></div>-->
						<!--</div>-->
					<!--</template>-->
				</el-autocomplete>
			</el-row>
			<el-row v-if="!!currentDatasheet">
				<div class="text-muted">Наименование файла:</div>
				<div class="file-info">{{ currentDatasheet.value }}</div>
				<div class="text-muted">Путь к файлу:</div>
				<div class="file-info">{{ currentDatasheet.file_url }}</div>
				<div class="text-muted">Комментарий:</div>
				<div class="file-info">{{ currentDatasheet.note }}</div>
			</el-row>
		</div>
	</div>
</template>

<script>

	export default {
		name: "UploaderRoot",
		props: {
			extNum: String,
			intNum: String,
			allowedFileSize: Number,
		},
		data() {
			return {
				isUploading: false,
				state: '',
				uploadNew: false,
				fileName: '',
				note: '',
				fileList: [],
				currentDatasheet: null,
				tempFileName: '',
			}
		},
		methods: {
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
						self.fileName = null;
						self.currentDatasheet = null;
					}
				});
			},
			handleExceed(files, fileList) {
				this.$message.warning(`За один раз можно загрузить только один файл`);
			},
			handleSuccess(response, file) {
				this.currentDatasheet = {
					label: null,
					value: file.name,
					file_url: `./site1.local/public/files/datasheets/`,
					note: this.note
				};
				this.tempFileName = JSON.parse(response).message;
				this.fileName = file.name;

				// TODO hack to indicate upload complete
				this.$children[3].$children[0].uploadFiles[0].status = 'success';
				this.isUploading = false;
			},
			handleAttachModeToggle() {
				this.currentDatasheet = null;
				this.fileName = '';
				this.state = '';
			},
			querySearchAsync(queryString, cb) {
				frappe.call({
					method: "dc_plc.controllers.role_file_uploader.search_existing_datasheets",
					args: {
						query: queryString,
					},
					callback: r => {
						cb(r.message);
					}
				});
			},
			handleAutocompleteSelect(item) {
				this.currentDatasheet = item;
			},
			handleUploadRequest(param) {
				this.isUploading = true;
				let url = "api/method/dc_plc.controllers.role_file_uploader.upload_file";
				let file = param.file;

				let form = new FormData();
				form.append("file", file);
				form.append("filename", file.name);
				form.append("test", "test data");

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
			// TODO asaasassaas
			upload_file(file, i) {
				this.currently_uploading = i;

				return new Promise((resolve, reject) => {
					let xhr = new XMLHttpRequest();
					xhr.upload.addEventListener('loadstart', (e) => {
						file.uploading = true;
					})
					xhr.upload.addEventListener('progress', (e) => {
						if (e.lengthComputable) {
							file.progress = e.loaded;
							file.total = e.total;
						}
					})
					xhr.upload.addEventListener('load', (e) => {
						file.uploading = false;
						resolve();
					})
					xhr.addEventListener('error', (e) => {
						file.failed = true;
						reject();
					})
					xhr.onreadystatechange = () => {
						if (xhr.readyState === XMLHttpRequest.DONE) {
							if (xhr.status === 200) {
								let r = null;
								let file_doc = null;
								try {
									r = JSON.parse(xhr.responseText);
									if (r.message.doctype === 'File') {
										file_doc = r.message;
									}
								} catch (e) {
									r = xhr.responseText;
								}

								file.doc = file_doc;

								if (this.on_success) {
									this.on_success(file_doc, r);
								}
							} else {
								file.failed = true;
								let error = null;
								try {
									error = JSON.parse(xhr.responseText);
								} catch (e) {
									// pass
								}
								frappe.request.cleanup({}, error);
							}
						}
					}
					xhr.open('POST', '/api/method/upload_file', true);
					xhr.setRequestHeader('Accept', 'application/json');
					xhr.setRequestHeader('X-Frappe-CSRF-Token', frappe.csrf_token);

					let form_data = new FormData();
					if (file.file_obj) {
						form_data.append('file', file.file_obj, file.name);
					}
					form_data.append('is_private', +file.private);
					form_data.append('folder', this.folder);

					if (file.file_url) {
						form_data.append('file_url', file.file_url);
					}

					if (this.doctype && this.docname) {
						form_data.append('doctype', this.doctype);
						form_data.append('docname', this.docname);
					}

					if (this.method) {
						form_data.append('method', this.method);
					}

					xhr.send(form_data);
				});
			}

		}
		// components: {
		// 	ExportWidget,
		// }
	}
</script>

<style>
	.el-row {
		margin-bottom: 15px;
	}

	.file-info {
		margin-bottom: 15px;
	}

	input[type="file"] {
		display: none;
	}
</style>