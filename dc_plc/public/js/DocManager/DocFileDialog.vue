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
					<el-option v-for="type in types" :label="type.label" :value="type.value"></el-option>
				</el-select>
			</el-form-item>
			<el-form-item label="Подтип файла">
				<el-select v-model="form.subtype" placeholder="Выберите подтип документа">
					<el-option v-for="sub in subtypes" :label="sub.label" :value="sub.value"></el-option>
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
				fileList: [],
				labelPosition: 'left',
				form: {
					id: null,
					name: '',
					type: '',
					subtype: '',
					note: 'note'
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
				let newSubs = this.typeSubtypeMap[this.form.type];
				this.form.subtype = newSubs[0].value;
				return newSubs;
			}
		},
		methods: {
			cancel() {
				console.log('cancel');
			},
			confirm() {
				console.log('confirm');
			},
		},
		watch: {
			formData(newVal, oldVal) {
				this.form = { ...this.formData };
			},
		},
		mounted: function () {
			this.form = { ...this.formData };
			this.form.type = 'DT001';
		}
	}
</script>

<style scoped>

</style>
