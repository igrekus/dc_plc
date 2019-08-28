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
				let title = frm.doc['title'];
				if (title !== file.file_name) {
					frm.set_value('title', file.file_name);
					frm.save();
				}
				frm.fields_dict['info_file'].wrapper.innerHTML =
					file.name ?
					'<span class="control-label">Метаданные файла</span><br/>' +
					`<span><a class="attached-file-link" target="_blank" href="/desk#Form/File/${file.name}">${file.file_name}</a></span>`
					:
					'<span class="control-label">Метаданные файла</span><br/><span>Файл не прикреплён</span>';
			}
		});
	}
});
