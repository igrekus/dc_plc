// Copyright (c) 2019, igrekus and contributors
// For license information, please see license.txt

frappe.ui.form.on('DC_Doc_Datasheet_List', {
	refresh: function(frm) {
		frm.fields_dict['tab_datasheet_meta'].grid.get_field('link_datasheet_meta').get_query = function (doc, cut, cdn) {
			return {
				query: 'dc_plc.controllers.file_manager.datasheet_search_query',
			}
		};
	},
});

frappe.ui.form.on('DC_Doc_Datasheets_in_Datasheet_List', {
	link_datasheet_meta: function(frm, cdt, cdn) {
		let row_id = locals[cdt][cdn]['link_datasheet_meta'];
		frappe.call({
			method: 'dc_plc.controllers.file_manager.get_datasheet_meta',
			args: {
				meta_id: row_id,
			},
			callback: r => {
				let meta_data = r.message;
				frappe.model.set_value(cdt, cdn, 'doc_type', meta_data['type_title']);
				frappe.model.set_value(cdt, cdn, 'file_name', meta_data['meta_title']);
			}
		});
	},
});
