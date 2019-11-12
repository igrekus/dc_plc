<template>
	<div>
		<el-form :model="form" :label-position="labelPosition" @submit.native.prevent>
			<el-form-item v-if="!!form.id" label="Название файла">
				<el-input v-model="form.name" autocomplete="off"></el-input>
			</el-form-item>
			<el-form-item v-else>
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
					<div class="el-upload__tip" slot="tip">PDF размером меньше 50 Мб</div>
				</el-upload>
			</el-form-item>
			<el-form-item label="Тип файла">
				<el-select v-model="form.type" placeholder="Выберите тип документа">
					<el-option label="КД" value="cd"></el-option>
					<el-option label="ТУ" value="op"></el-option>
				</el-select>
			</el-form-item>
			<el-form-item label="Подтип файла">
				<el-select v-model="form.subtype" placeholder="Выберите подтип документа">
					<el-option label="Zone No.1" value="ccd"></el-option>
				</el-select>
			</el-form-item>
			<div>form customization stub</div>
			<el-form-item label="Комментарий">
				<el-input v-model="form.note" type="textarea" autosize>
				</el-input>
			</el-form-item>
		</el-form>
		<div>
			product link section
		</div>
		<el-input placeholder="Поиск устройства"></el-input>
		<table>
			<tr><th>product_id</th><th>ext_name</th><th>int_name</th></tr>
			<tr><td>1</td><td>2</td><td>3</td></tr>
		</table>
		<span slot="footer" class="dialog-footer">
			<el-button @click="cancel">Cancel</el-button>
			<el-button type="primary" @click="confirm">Confirm</el-button>
		</span>
	</div>
</template>

<script>
	export default {
		name: 'DocFileDialog',
		props: ['formData'],
		data() {
			return {
				labelPosition: 'left',
				form: {
					id: null,
					name: '',
					type: 'cd',
					subtype: 'ccd',
					note: 'note'
				},
			}
		},
		methods: {
			cancel() {
				console.log('cancel');
			},
			confirm() {
				console.log('confirm');
			}
		},
		watch: {
			formData(newVal, oldVal) {
				this.form = { ...this.formData };
				console.log(newVal, oldVal);
			},
		},
		mounted: function () {
			this.form = { ...this.formData };
		}
	}
</script>

<style scoped>

</style>
