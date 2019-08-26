// Copyright (c) 2019, igrekus and contributors
// For license information, please see license.txt

frappe.ui.form.on('DC_Doc_Datasheet_Meta', {
	refresh: frm => {
		frappe.call({
			method: 'dc_plc.controllers.file_manager.get_file_meta',
			args: {
				doctype: frm.doctype,
				docname: frm.docname,
				field_name: 'attached_file'
			},
			callback: r => {
				let file = r.message;
				frm.fields_dict['info_file'].wrapper.innerHTML =
					'<span class="control-label">Метаданные файла</span><br/>' +
					`<span><a class="attached-file-link" target="_blank" href="/desk#Form/File/${file.name}">test_datasheet.txt</a></span>`;
			}
		});
	}
});
