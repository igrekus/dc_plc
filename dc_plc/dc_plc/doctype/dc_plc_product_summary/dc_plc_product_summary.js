// Copyright (c) 2018, igrekus and contributors
// For license information, please see license.txt

let value_or_none = frappe.dc_plc.utils.value_or_none;
let set_field_title = frappe.dc_plc.utils.ui.set_field_title;
let set_info_field = frappe.dc_plc.utils.ui.set_info_field;
let render_info_field = frappe.dc_plc.utils.ui.render_info_field;
let render_field_title = frappe.dc_plc.utils.ui.render_field_title;


let render_step_info = (frm) => {
	frappe.call({
		method: 'dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary.get_step_info',
		args: {
			prod_id: frm.doc.name,
		},
		callback: r => {
			console.log(r.message);
			render_info_field(frm, 'info_step', 'Шаг ЖЦИ', r.message);
		}
	});
};


frappe.ui.form.on('DC_PLC_Product_Summary', {
	refresh: frm => {
		frm.fields_dict['tab_consultants'].grid.get_field('link_employee').get_query = function (doc, cut, cdn) {
			return {
				query: 'dc_plc.controllers.queries.consultant_query'
			}
		};
		frm.fields_dict['tab_developers'].grid.get_field('link_employee').get_query = function (doc, cut, cdn) {
			return {
				query: 'dc_plc.controllers.queries.developer_query'
			}
		};

		set_field_title(frm, 'link_function');
		set_field_title(frm, 'link_package');
		set_field_title(frm, 'link_rnd_project');
		set_field_title(frm, 'link_type');
		set_field_title(frm, 'link_status');
		set_field_title(frm, 'link_letter');
		set_field_title(frm, 'link_step');

		set_info_field(frm, 'link_function', 'Функция');
		set_info_field(frm, 'link_rnd_project', 'Наименование ОКР');

		render_info_field(frm, 'info_ext_num', 'Внешний номер', value_or_none(frm.get_field('ext_num').value));
		render_info_field(frm, 'info_int_num', 'Внутренний номер', value_or_none(frm.get_field('int_num').value));
		render_info_field(frm, 'info_description', 'Описание', value_or_none(frm.get_field('description').value).split('\n').join('<br>'));
		render_info_field(frm, 'info_specs', 'Параметры', value_or_none(frm.get_field('specs').value).split('\n').join('<br>'));
		render_step_info(frm);

		// fields by section: 1 - 3, 2 - 1, 3 - 10, 4 - 2, 5 - 1, 6 - 2, 7 - 2
		let relevant = 0;
		let total = 21;

		relevant += frm.doc.rel_check_dept_head ? 3 : 0;
		relevant += frm.doc.rel_check_rnd_spec ? 1 : 0;
		relevant += frm.doc.rel_check_developer ? 10 : 0;
		relevant += frm.doc.rel_check_opcon ? 2 : 0;
		relevant += frm.doc.rel_check_procmap ? 1 : 0;
		relevant += frm.doc.rel_check_tech_writer ? 2 : 0;
		relevant += frm.doc.rel_check_desdoc ? 2 : 0;
		let percent = Math.round((relevant / total) * 100);

		frm.fields_dict['info_rel_total'].wrapper.innerHTML = '<span class="text-muted">Актуально:</span>&nbsp;<span>' + percent + '%</span>';

		// TODO add grid button logic here
		// prepare grid buttons
		// tech writer -- datasheet grid
		frm.fields_dict['tab_datasheet'].grid.add_custom_button('Добавить даташит', () => {
			upload_datasheet({
				frm: frm,
				product: frm.doc,
			});
		});
		let tech_writer_grid = $('.form-group*[data-fieldname="tab_datasheet"]');
		tech_writer_grid.find('.btn.grid-add-row').hide();
		// tech_writer_grid.find('.btn.grid-remove-rows').hide();

		// developer -- dev report grid
		frm.fields_dict['tab_dev_report'].grid.add_custom_button('Добавить отчёт', () => {
			upload_dev_report({
				frm: frm,
				product: frm.doc,
			})
		});
		let dev_report_grid = $('.form-group*[data-fieldname="tab_dev_report"]');
		dev_report_grid.find('.btn.grid-add-row').hide();
		// dev_report_grid.find('.btn.grid-remove-rows').hide();

		// anybody -- misc file grid
		frm.fields_dict['tab_misc'].grid.add_custom_button('Добавить файл', () => {
			upload_misc({
				frm: frm,
				product: frm.doc,
			})
		});
		let misc_grid = $('.form-group*[data-fieldname="tab_misc"]');
		misc_grid.find('.btn.grid-add-row').hide();
		// misc_grid.find('.btn.grid-remove-rows').hide();

		// opcon specialist -- opcon grid
		frm.fields_dict['tab_opcon'].grid.add_custom_button('Добавить файл', () => {
			upload_opcon({
				frm: frm,
				product: frm.doc,
			})
		});
		let opcon_grid = $('.form-group*[data-fieldname="tab_opcon"]');
		opcon_grid.find('.btn.grid-add-row').hide();
		// misc_grid.find('.btn.grid-remove-rows').hide();

		// desdoc specialist -- desdoc grid
		frm.fields_dict['tab_desdoc'].grid.add_custom_button('Добавить файл', () => {
			upload_desdoc({
				frm: frm,
				product: frm.doc,
			})
		});
		let desdoc_grid = $('.form-group*[data-fieldname="tab_desdoc"]');
		desdoc_grid.find('.btn.grid-add-row').hide();
		// desdoc_grid.find('.btn.grid-remove-rows').hide();


	},
	ext_num: frm => render_info_field(frm, 'info_ext_num', 'Внешний номер', value_or_none(frm.get_field('ext_num').value)),
	int_num: frm => render_info_field(frm, 'info_int_num', 'Внутренний номер', value_or_none(frm.get_field('int_num').value)),
	link_function: frm => {
		let field = 'link_function';
		frappe.db.get_doc(frm.fields_dict[field].df.options, frm.fields_dict[field].value).then(result => {
			render_field_title(frm, field, value_or_none(result.title));
			render_info_field(frm, 'info_function', 'Функция', value_or_none(result.title));
		});
	},
	link_rnd_project: frm => {
		let field = 'link_rnd_project';
		frappe.db.get_doc(frm.fields_dict[field].df.options, frm.fields_dict[field].value).then(result => {
			render_field_title(frm, field, value_or_none(result.title));
			render_info_field(frm, 'info_rnd_project', 'Функция', value_or_none(result.title));
		});
	},
	link_package: frm => {
		let field = 'link_package';
		frappe.db.get_doc(frm.fields_dict[field].df.options, frm.fields_dict[field].value).then(result => {
			render_field_title(frm, field, value_or_none(result.title));
		});
	},
	link_type: frm => {
		let field = 'link_type';
		frappe.db.get_doc(frm.fields_dict[field].df.options, frm.fields_dict[field].value).then(result => {
			render_field_title(frm, field, value_or_none(result.title));
		});
	},
	link_status: frm => {
		let field = 'link_status';
		frappe.db.get_doc(frm.fields_dict[field].df.options, frm.fields_dict[field].value).then(result => {
			render_field_title(frm, field, value_or_none(result.title));
		});
	},
	link_step: frm => {
		let field = 'link_step';
		frappe.db.get_doc(frm.fields_dict[field].df.options, frm.fields_dict[field].value).then(result => {
			render_field_title(frm, field, value_or_none(result.title));
		});
	},
	link_letter: frm => {
		let field = 'link_letter';
		frappe.db.get_doc(frm.fields_dict[field].df.options, frm.fields_dict[field].value).then(result => {
			render_field_title(frm, field, value_or_none(result.title));
		});
	},
	description: frm => {
		render_info_field(frm, 'info_description', 'Описание', value_or_none(frm.get_field('description').value).split('\n').join('<br>'));
	},
	specs: frm => {
		render_info_field(frm, 'info_specs', 'Параметры', value_or_none(frm.get_field('specs').value).split('\n').join('<br>'));
	},
	// relevance checks
	rel_check_dept_head: frm => {
		if (frm.fields_dict['rel_check_dept_head'].value) {
			frm.set_value('rel_date_dept_head', frappe.datetime.now_date());
		} else {
			frm.set_value('rel_date_dept_head', '0001-01-01');
		}
	},
	rel_check_rnd_spec: frm => {
		if (frm.fields_dict['rel_check_rnd_spec'].value) {
			frm.set_value('rel_date_rnd_spec', frappe.datetime.now_date());
		} else {
			frm.set_value('rel_date_rnd_spec', '0001-01-01');
		}
	},
	rel_check_developer: frm => {
		if (frm.fields_dict['rel_check_developer'].value) {
			frm.set_value('rel_date_developer', frappe.datetime.now_date());
		} else {
			frm.set_value('rel_date_developer', '0001-01-01');
		}
	},
	rel_check_opcon: frm => {
		if (frm.fields_dict['rel_check_opcon'].value) {
			frm.set_value('rel_date_opcon', frappe.datetime.now_date());
		} else {
			frm.set_value('rel_date_opcon', '0001-01-01');
		}
	},
	rel_check_procmap: frm => {
		if (frm.fields_dict['rel_check_procmap'].value) {
			frm.set_value('rel_date_procmap', frappe.datetime.now_date());
		} else {
			frm.set_value('rel_date_procmap', '0001-01-01');
		}
	},
	rel_check_tech_writer: frm => {
		if (frm.fields_dict['rel_check_tech_writer'].value) {
			frm.set_value('rel_date_tech_writer', frappe.datetime.now_date());
		} else {
			frm.set_value('rel_date_tech_writer', '0001-01-01');
		}
	},
	rel_check_desdoc: frm => {
		if (frm.fields_dict['rel_check_desdoc'].value) {
			frm.set_value('rel_date_desdoc', frappe.datetime.now_date());
		} else {
			frm.set_value('rel_date_desdoc', '0001-01-01');
		}
	},
});

let serve_document = (frm, cdt, cdn) => {
	let row = frappe.model.get_doc(cdt, cdn);
	open_url_post('/api/method/dc_plc.controllers.file_manager.serve_document', { meta_id: row.link_doc_meta }, false);
};

frappe.ui.form.on('DC_Doc_Datasheets_in_Datasheet_List', {
	link_datasheet_meta: function (frm, cdt, cdn) {
		let row_id = locals[cdt][cdn]['link_datasheet_meta'];
		frappe.call({
			method: 'dc_plc.controllers.file_manager.get_datasheet_meta',
			args: {
				meta_id: row_id,
			},
			callback: r => {
				let meta_data = r.message;
				frappe.model.set_value(cdt, cdn, 'doc_type', meta_data['type_title']);
				frappe.model.set_value(cdt, cdn, 'doc_subtype', meta_data['subtype_title']);
				frappe.model.set_value(cdt, cdn, 'file_name', meta_data['meta_title']);
			}
		});
	},
	btn_download: serve_document,
});


frappe.ui.form.on('DC_Doc_Dev_Report_in_Dev_Report_List', {
	btn_download: serve_document,
});


frappe.ui.form.on('DC_Doc_Misc_in_Misc_List', {
	btn_download: serve_document,
});


frappe.ui.form.on('DC_Doc_Opcon_in_Opcon_List', {
	btn_download: serve_document,
});


frappe.ui.form.on('DC_Doc_Desdoc_in_Desdoc_List', {
	btn_download: serve_document,
});


let upload_datasheet = ({frm, product}) => {
	new frappe.dc_plc.RoleFileUploader({
		form: frm,
		product: product,
		title: 'Добавить даташит',
		method: 'dc_plc.controllers.role_file_uploader.add_datasheet',
		fileType: 'datasheets',   // this will be the storage directory name and a part of the temp file name
		searchMethod: 'dc_plc.controllers.role_file_uploader.search_existing_datasheets',
	});
};

let upload_dev_report = ({frm, product}) => {
	new frappe.dc_plc.RoleFileUploader({
		form: frm,
		product: product,
		title: 'Добавить отчёт разработчика',
		method: 'dc_plc.controllers.role_file_uploader.add_dev_report',
		fileType: 'dev_reports',
		searchMethod: 'dc_plc.controllers.role_file_uploader.search_existing_dev_reports',
	});
};

let upload_misc = ({frm, product}) => {
	new frappe.dc_plc.RoleFileUploader({
		form: frm,
		product: product,
		title: 'Добавить документ',
		method: 'dc_plc.controllers.role_file_uploader.add_misc',
		fileType: 'misc',
		searchMethod: 'dc_plc.controllers.role_file_uploader.search_existing_misc',
	});
};

let upload_opcon = ({frm, product}) => {
	new frappe.dc_plc.RoleFileUploader({
		form: frm,
		product: product,
		title: 'Добавить ТУ',
		method: 'dc_plc.controllers.role_file_uploader.add_opcon',
		fileType: 'opcons',
		searchMethod: 'dc_plc.controllers.role_file_uploader.search_existing_opcon',
		subtypeMethod: 'dc_plc.controllers.role_file_uploader.get_opcon_subtypes'
	});
};

let upload_desdoc = ({frm, product}) => {
	new frappe.dc_plc.RoleFileUploader({
		form: frm,
		product: product,
		title: 'Добавить КД',
		method: 'dc_plc.controllers.role_file_uploader.add_desdoc',
		fileType: 'desdocs',
		searchMethod: 'dc_plc.controllers.role_file_uploader.search_existing_desdoc',
		subtypeMethod: 'dc_plc.controllers.role_file_uploader.get_desdoc_subtypes'
	});
};


// List of Triggers
//
// Field Names (see the company example above)
// setup
// onload
// refresh
// validate
// on_submit
// onload_post_render
// Child Table Triggers (need to be on the subtable DocType)
//
// fieldname_add
// fieldname_move
// fieldname_before_remove
// fieldname_remove
// these also work: https://developer.mozilla.org/en-US/docs/Web/Events

// frappe.ui.form.on("Purchase Order", "refresh", function(frm) {
//     cur_frm.set_query("supplier", function() {
//         return {
//             "filters": {
//                 "currency_pay_in": "USD"
//             }
//         };
//     });
// });

