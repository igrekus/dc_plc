// Copyright (c) 2018, igrekus and contributors
// For license information, please see license.txt

frappe.ui.form.on('DC_PLC_Product_Summary', {
    refresh: frm => {
        cur_frm.fields_dict['tab_consultants'].grid.get_field('link_employee').get_query = function(doc, cut, cdn) {
            return {
                query: 'dc_plc.controllers.queries.consultant_query'
            }
        };
        cur_frm.fields_dict['tab_developers'].grid.get_field('link_employee').get_query = function(doc, cut, cdn) {
            return {
                query: 'dc_plc.controllers.queries.developer_query'
            }
        }
    },
    // fire an event on property update
    link_package: frm => {
        // // console.log(frm.fields_dict['link_package'].$input);
        // let value = frm.fields_dict['link_package'].value;
        // let list = frm.fields_dict['link_package'].awesomplete._list;
        // if (typeof value !== 'undefined') {
        //     list.forEach( ( {description, val, label} ) => {
        //         if (value === label) {
        //             console.log('found package:', label, description);
        //             cur_frm.fields_dict['link_package'].$input.value = description;
        //         }
        //     });
        // }
    }
    // frappe.ui.form.on(this.frm.doctype, 'set_posting_date_and_time_read_only', function(frm) {
    // frappe.ui.form.on(this.frm.doctype, 'set_posting_time', function(frm) {
    // frappe.ui.form.on(this.frm.doctype + " Item", "rate", function(frm, cdt, cdn) {
    // cur_frm.events[fieldname] = handler;
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

