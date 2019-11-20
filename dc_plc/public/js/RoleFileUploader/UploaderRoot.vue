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
					<div class="el-upload__text">Для загрузки, <em>перетащите</em> файл или <em>нажмите</em> мышкой</div>
					<div class="el-upload__tip" slot="tip">Ограничение по размеру файла -- 50 Мб</div>
				</el-upload>
			</el-row>
			<div v-if="!!subtypeMethod">
				<el-row>
					<el-select v-model="selectedSubtype" placeholder="Тип файла">
						<el-option
								v-for="item in subtypeOptions"
								:key="item.value"
								:label="item.label"
								:value="item.value">
						</el-option>
					</el-select>
				</el-row>
				<el-row>
					<el-input
							placeholder="Номер"
							v-model="opconNum"/>
				</el-row>
				<div v-if="fileType === 'opcons'">
					<el-row>
						<el-input
								placeholder="Внутренний номер ТУ"
								v-model="opconIntNum"/>
					</el-row>
					<el-row>
						<el-date-picker
								v-model="dateApproval"
								type="date"
								placeholder="Дата утверждения">
						</el-date-picker>
					</el-row>
				</div>
				<el-row>
					<el-date-picker
							v-model="dateArchive"
							type="date"
							placeholder="Дата сдачи в архив">
					</el-date-picker>
				</el-row>
				<el-row>
					<el-input
							type="textarea"
							autosize
							placeholder="Комментарий"
							v-model="note"/>
				</el-row>
			</div>
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
			<el-row v-if="!!currentUpload">
				<div class="text-muted">Наименование файла:</div>
				<div class="file-info">{{ currentUpload.value }}</div>
				<div class="text-muted">Путь к файлу:</div>
				<div class="file-info">{{ currentUpload.file_url }}</div>
				<div class="text-muted">Комментарий:</div>
				<div class="file-info">{{ currentUpload.note }}</div>
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
			fileType: String,
			searchMethod: String,
			subtypeMethod: String,
		},
		data() {
			return {
				isUploading: false,
				state: '',
				uploadNew: false,
				fileName: '',
				note: '',
				opconNum: '',
				opconIntNum: '',
				dateApproval: '',
				dateArchive: '',
				fileList: [],
				currentUpload: null,
				tempFileName: '',
				subtypeOptions: [],
				selectedSubtype: '',
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
						self.currentUpload = null;
					}
				});
			},
			handleExceed(files, fileList) {
				this.$message.warning(`За один раз можно загрузить только один файл`);
			},
			handleSuccess(response, file) {
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
			handleAttachModeToggle() {
				this.currentUpload = null;
				this.fileName = '';
				this.state = '';
			},
			querySearchAsync(queryString, cb) {
				frappe.call({
					method: this.searchMethod,
					args: {
						query: queryString,
					},
					callback: r => {
						cb(r.message);
					}
				});
			},
			handleAutocompleteSelect(item) {
				this.currentUpload = item;
			},
			handleUploadRequest(param) {
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
			note(new_v, old_v) {
				if (!this.currentUpload)
					return;
				this.currentUpload.note = new_v;
			},
			selectedSubtype(new_v, old_v) {
				if (!this.currentUpload)
					return;
				this.currentUpload.subtype = new_v;
			},
			opconNum(new_v, old_v) {
				if (!this.currentUpload)
					return;
				this.currentUpload.opconNum = new_v;
			},
			opconIntNum(new_v, old_v) {
				if (!this.currentUpload)
					return;
				this.currentUpload.opconIntNum = new_v;
			},
			dateApproval(new_v, old_v) {
				if (!this.currentUpload)
					return;
				this.currentUpload.dateApproval = new_v;
			},
			dateArchive(new_v, old_v) {
				if (!this.currentUpload)
					return;
				this.currentUpload.dateArchive = new_v;
			}
		},
		mounted() {
			if (!this.subtypeMethod)
				return;

			let me = this;
			frappe.call({
				method: this.subtypeMethod,
				args: {},
				callback: r => {
					me.subtypeOptions = r.message;
					me.selectedSubtype = me.subtypeOptions[0].value;
				}
			});
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