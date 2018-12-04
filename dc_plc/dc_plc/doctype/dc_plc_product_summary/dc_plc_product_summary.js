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
    }
});

// frappe.ui.form.on("Purchase Order", "refresh", function(frm) {
//     cur_frm.set_query("supplier", function() {
//         return {
//             "filters": {
//                 "currency_pay_in": "USD"
//             }
//         };
//     });
// });

