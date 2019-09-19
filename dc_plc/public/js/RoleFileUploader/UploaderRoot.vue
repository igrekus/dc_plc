<template>
	<div>
		{{ intNum }}
		{{ extNum }}
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
				<div class="text-muted">Имя файла</div>
				<el-input v-model="fileName"/>
			</el-row>
			<el-row>
				<el-input
						type="textarea"
						autosize
						placeholder="Введите комментарий..."
						v-model="note" />
			</el-row>
			<el-row>
				<el-upload
						class="upload-demo"
						drag
						action="https://jsonplaceholder.typicode.com/posts/"
						:limit="1"
						:before-upload="beforeUpload"
						:on-remove="handleRemove"
						:on-exceed="handleExceed"
						:on-success="handleSuccess"
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
				<div class="text-muted">Примечание:</div>
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
				state: '',
				uploadNew: false,
				fileName: '',
				note: '',
				fileList: [],
				currentDatasheet: null
			}
		},
		methods: {
			beforeUpload(file) {
				const { size } = file;
				const isAllowedSize = (size / 1024 / 1024) < this.allowedFileSize;

				if (!isAllowedSize) {
					this.$message.warning(`Размер файла не должен превышать 10 Мб`);
				}
				return isAllowedSize;
			},
			handleRemove() {
				console.log('handle remove');
			},
			handleExceed(files, fileList) {
				this.$message.warning(`За раз можно загрузить только 1 файл`);
			},

			handleSuccess(result, file) {
				console.log('handle success');
				this.currentDatasheet = {
					label: 'id',
					value: 'title',
					file_url: 'file/url',
					note: 'noteeee'
				}
				// 	/*
				// 		  handleAvatarSuccess(res, file) {
				// this.imageUrl = URL.createObjectURL(file.raw);
				// },*/
			},
			handleAttachModeToggle() {
				this.currentDatasheet = null;
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