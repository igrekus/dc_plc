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
    // fire an even on property update
    link_package: frm => {
        // console.log(frm.fields_dict['link_package'].$input);
        let value = frm.fields_dict['link_package'].value;
        let list = frm.fields_dict['link_package'].awesomplete._list;
        if (typeof value !== 'undefined') {
            list.forEach( ( {description, val, label} ) => {
                if (value === label) {
                    console.log('found package:', label, description);
                }
            });
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

