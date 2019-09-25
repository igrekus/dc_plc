import UploaderRoot from './UploaderRoot.vue';

frappe.provide('frappe.dc_plc');

frappe.dc_plc.RoleFileUploader = class {
	constructor({
		product,
		wrapper,
		method,
		on_success,
		doctype,
		docname,
		files,
		folder,
		restrictions,
		upload_notes,
		allow_multiple,
		as_dataurl
	} = {}) {
		this.product = product;

		this.make_dialog({
			title: 'Добавить даташит'
		});

		this.$fileuploader = new Vue({
			el: this.wrapper,
			render: h => h(UploaderRoot, {
				props: {
					extNum: product['ext_num'],
					intNum: product['int_num'],
					allowedFileSize: 10,
					// show_upload_button: !Boolean(this.dialog),
					// doctype,
					// docname,
					// method,
					// folder,
					// on_success,
					// restrictions,
					// upload_notes,
					// allow_multiple,
					// as_dataurl
				}
			})
		});

		this.uploader = this.$fileuploader.$children[0];

		// if (files && files.length) {
		// 	this.uploader.add_files(files);
		// }
	}

	upload_files() {
		let datasheet = this.uploader.currentDatasheet;
		let tempFileName = this.uploader.tempFileName;
		if (!datasheet) {
			return;
		}

		console.log(datasheet);
		console.log(tempFileName);

		let self = this;
		frappe.call({
			method: "dc_plc.controllers.role_file_uploader.add_datasheet",
			args: {
				prod_id: self.product.name,
				datasheet: self.uploader.currentDatasheet,
				temp_file: self.uploader.tempFileName
			},
			callback: function (r) {
				console.log(r.message);
				// this.dialog && this.dialog.hide();
			}
		});
		// this.dialog && this.dialog.get_primary_btn().prop('disabled', true);
		// return this.uploader.upload_files()
		// 	.then(() => {
		// 		this.dialog && this.dialog.hide();
		// 	});
	}

	make_dialog({title, } = {}) {
		this.dialog = new frappe.ui.Dialog({
			title: title,
			fields: [
				{
					fieldtype: 'HTML',
					fieldname: 'dialog_content'
				}
			],
			primary_action_label: 'Добавить',
			primary_action: () => {
				this.upload_files();
			}
		});

		this.wrapper = this.dialog.fields_dict['dialog_content'].$wrapper[0];
		this.dialog.show();
		this.dialog.$wrapper.on('hidden.bs.modal', function() {
			$(this).data('bs.modal', null);
			$(this).remove();
		});
	}
};
