// Copyright (c) 2018, igrekus and contributors
// For license information, please see license.txt

let value_or_none = value => {
    return value ? value : 'отсутствует';
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

        let set_title = title => {
            if (!frm.fields_dict[title].value)
                return;
            frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
                let field = frm.fields_dict[title];
                field.label_span.innerHTML = __(field._label) + '&nbsp-&nbsp <b>' + value_or_none(result.title) + '</b>';
            });
        };

        let set_info = (field, title) => {
            if (!frm.fields_dict[field].value)
                return;
            frappe.db.get_doc(frm.fields_dict[field].df.options, frm.fields_dict[field].value).then(result => {
                frm.fields_dict[field.replace('link_', 'info_')].wrapper.innerHTML =
                    '<span class="text-muted">' + title + '</span><br/>' +
                    '<span>' + value_or_none(result.title) + '</span>';
            });
        };

        set_title('link_function');
        set_title('link_package');
        set_title('link_rnd_project');
        set_title('link_type');
        set_title('link_status');
        set_title('link_letter');

        frm.fields_dict['info_ext_num'].wrapper.innerHTML =
            '<span class="text-muted">Внешний номер</span><br/>' +
            '<span>' + value_or_none(frm.get_field('ext_num').value) + '</span>';
        frm.fields_dict['info_int_num'].wrapper.innerHTML =
            '<span class="text-muted">Внутренний номер</span><br/>' +
            '<span>' + value_or_none(frm.get_field('int_num').value) + '</span>';
        frm.fields_dict['info_description'].wrapper.innerHTML =
            '<span class="text-muted">Описание</span><br/>' +
            '<span>' + value_or_none(frm.get_field('description').value).split('\n').join('<br>') + '</span>';
        frm.fields_dict['info_specs'].wrapper.innerHTML =
            '<span class="text-muted">Параметры</span><br/>' +
            '<span>' + value_or_none(frm.get_field('specs').value).split('\n').join('<br>') + '</span>';
        set_info('link_function', 'Функция');
        set_info('link_rnd_project', 'Наименование ОКР');

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
    },
    ext_num: frm => frm.fields_dict['info_ext_num'].wrapper.innerHTML =
        '<span class="text-muted">Внешний номер</span><br/>' +
        '<span>' + value_or_none(frm.get_field('ext_num').value) + '</span>',
    int_num: frm => frm.fields_dict['info_int_num'].wrapper.innerHTML =
        '<span class="text-muted">Внутренний номер</span><br/>' +
        '<span>' + value_or_none(frm.get_field('int_num').value) + '</span>',
    link_function: frm => {
        let title = 'link_function';
        frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
            let field = frm.fields_dict[title];
            let msg = value_or_none(result.title);
            field.label_span.innerHTML = __(field._label) + '&nbsp-&nbsp <b>' + msg + '</b>';
            frm.fields_dict['info_function'].wrapper.innerHTML =
                '<span class="text-muted">Функция</span><br/>' +
                '<span>' + msg + '</span>';
        });
    },
    link_package: frm => {
        let title = 'link_package';
        frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
            let field = frm.fields_dict[title];
            field.label_span.innerHTML = __(field._label) + '&nbsp-&nbsp <b>' + value_or_none(result.title) + '</b>';
        });
    },
    link_rnd_project: frm => {
        let title = 'link_rnd_project';
        frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
            let field = frm.fields_dict[title];
            let msg = value_or_none(result.title);
            field.label_span.innerHTML = __(field._label) + '&nbsp-&nbsp <b>' + msg + '</b>';
            frm.fields_dict['info_rnd_project'].wrapper.innerHTML =
                '<span class="text-muted">Наименование ОКР</span><br/>' +
                '<span>' + msg + '</span>';
        });
    },
    link_type: frm => {
        let title = 'link_type';
        frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
            let field = frm.fields_dict[title];
            field.label_span.innerHTML = __(field._label) + '&nbsp-&nbsp <b>' + value_or_none(result.title) + '</b>';
        });
    },
    link_status: frm => {
        let title = 'link_status';
        frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
            let field = frm.fields_dict[title];
            field.label_span.innerHTML = __(field._label) + '&nbsp-&nbsp <b>' + value_or_none(result.title) + '</b>';
        });
    },
    link_letter: frm => {
        let title = 'link_letter';
        frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
            let field = frm.fields_dict[title];
            field.label_span.innerHTML = __(field._label) + '&nbsp-&nbsp <b>' + value_or_none(result.title) + '</b>';
        });
    },
    description: frm => {
        frm.fields_dict['info_description'].wrapper.innerHTML =
            '<span class="text-muted">Описание</span><br/>' +
            '<span>' + value_or_none(frm.get_field('description').value).split('\n').join('<br>') + '</span>';
    },
    specs: frm => {
        frm.fields_dict['info_specs'].wrapper.innerHTML =
            '<span class="text-muted">Параметры</span><br/>' +
            '<span>' + value_or_none(frm.get_field('specs').value).split('\n').join('<br>') + '</span>';
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
                console.log(meta_data);
                console.log(frappe.model.get_doc(cdt, cdn));
                frappe.model.set_value(cdt, cdn, 'doc_type', meta_data['type_title']);
                frappe.model.set_value(cdt, cdn, 'doc_subtype', meta_data['subtype_title']);
                frappe.model.set_value(cdt, cdn, 'file_name', meta_data['meta_title']);
            }
        });
    },
});

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

