// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

// TODO DRY this crap from all queries
let check_handle = (o) => {
	let relevant = o.checked;
	let name = o.id;
	frappe.call({
		method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary.set_dept_head_relevant",
		args: {
			name: name,
            relevant: relevant ? 1 : 0,
        },
        callback: r => {
            let {date, check} = r.message;
            $('.rel_label_' + name)[0].innerHTML = "&nbsp;&nbsp;" + date;
            o.checked = !!check;
        }
    });
};

// let higlight_column = (col_num) => {
//     let relevant_color = '#f2f4f6';
//     $('.dt-cell__content.dt-cell__content--col-' + String(col_num)).css('backgroundColor', relevant_color);
// };

frappe.query_reports["DC Product MMIC Dept Head Stats"] = {
    filters: [],
    // formatter: (value, row, column, row_data, format) => {
    //     let new_value = '';
    //
    //     console.log(column);
    //
    //     if (!value) {
    //         return new_value;
    //     }
    //     if (column.id === __('Relevance')) {
    //         return value;
    //     }
    //
    //     new_value = `<a href="${window.location.host}/desk#Form/DC_PLC_Product_Summary/${row_data.ID}">${value}</a>`;
    //
    //     return new_value;
    // },
    // onload: report => {
    //     // TODO hack, use API to highlight cols
    //     setTimeout(() => {
    //         higlight_column(4);
    //         higlight_column(6);
    //         higlight_column(7);
    //     }, 1500);
    // }
};
