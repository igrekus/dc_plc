// Copyright (c) 2018, igrekus and contributors
// For license information, please see license.txt

frappe.ui.form.on('DC_PLC_Product_Summary', {
    refresh: frm => {
        frm.fields_dict['tab_consultants'].grid.get_field('link_employee').get_query = function(doc, cut, cdn) {
            return {
                query: 'dc_plc.controllers.queries.consultant_query'
            }
        };
        frm.fields_dict['tab_developers'].grid.get_field('link_employee').get_query = function(doc, cut, cdn) {
            return {
                query: 'dc_plc.controllers.queries.developer_query'
            }
        };

        let set_title = title => {
            if (!frm.fields_dict[title].value)
                return;
            frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
                let field = frm.fields_dict[title];
                field.label_span.innerHTML = __(field._label) + '&nbsp-&nbsp <b>' + result.title + '</b>';
            });
        };

        let set_info = (field, title) => {
            if (!frm.fields_dict[field].value)
                return;
            frappe.db.get_doc(frm.fields_dict[field].df.options, frm.fields_dict[field].value).then(result => {
                frm.fields_dict[field.replace('link_', 'info_')].wrapper.innerHTML = '<span class="text-muted">' + title + '</span><br/><span>' + result.title + '</span>';
            });
        };

        set_title('link_function');
        set_title('link_package');
        set_title('link_rnd_project');
        set_title('link_type');

        frm.fields_dict['info_ext_num'].wrapper.innerHTML = '<span class="text-muted">Внешний номер</span><br/><span>' + frm.get_field('ext_num').value + '</span>';
        frm.fields_dict['info_int_num'].wrapper.innerHTML = '<span class="text-muted">Внутренний номер</span><br/><span>' + frm.get_field('int_num').value + '</span>';
        set_info('link_function', 'Функция');
        set_info('link_rnd_project', 'Наименование ОКР');
        frm.fields_dict['info_description'].wrapper.innerHTML = '<span class="text-muted">Описание</span><br/><span>' + frm.get_field('description').value.split('\n').join('<br>') + '</span>';
        frm.fields_dict['info_specs'].wrapper.innerHTML = '<span class="text-muted">Параметры</span><br/><span>' + frm.get_field('specs').value.split('\n').join('<br>') + '</span>';
    },
    ext_num: frm => frm.fields_dict['info_ext_num'].wrapper.innerHTML = '<span class="text-muted">Внешний номер</span><br/><span>' + frm.get_field('ext_num').value + '</span>',
    int_num: frm => frm.fields_dict['info_int_num'].wrapper.innerHTML = '<span class="text-muted">Внутренний номер</span><br/><span>' + frm.get_field('int_num').value + '</span>',
    link_function: frm => {
        let title = 'link_function';
        frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
            let field = frm.fields_dict[title];
            field.label_span.innerHTML = __(field._label) + '&nbsp-&nbsp <b>' + result.title + '</b>';
            frm.fields_dict['info_function'].wrapper.innerHTML = '<span class="text-muted">Функция</span><br/><span>' + result.title + '</span>';
        });
    },
    link_package: frm => {
        let title = 'link_package';
        frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
            let field = frm.fields_dict[title];
            field.label_span.innerHTML = __(field._label) + '&nbsp-&nbsp <b>' + result.title + '</b>';
        });
    },
    link_rnd_project: frm => {
        let title = 'link_rnd_project';
        frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
            let field = frm.fields_dict[title];
            field.label_span.innerHTML = __(field._label) + '&nbsp-&nbsp <b>' + result.title + '</b>';
            frm.fields_dict['info_rnd_project'].wrapper.innerHTML = '<span class="text-muted">Наименование ОКР</span><br/><span>' + result.title + '</span>';
        });
    },
    link_type: frm => {
        let title = 'link_type';
        frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
            let field = frm.fields_dict[title];
            field.label_span.innerHTML = __(field._label) + '&nbsp-&nbsp <b>' + result.title + '</b>';
        });
    },
    description: frm => {
        frm.fields_dict['info_description'].wrapper.innerHTML = '<span class="text-muted">Описание</span><br/><span>' + frm.get_field('description').value.split('\n').join('<br>') + '</span>';
    },
    specs: frm => {
        frm.fields_dict['info_specs'].wrapper.innerHTML = '<span class="text-muted">Параметры</span><br/><span>' + frm.get_field('specs').value.split('\n').join('<br>') + '</span>';
    }
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

