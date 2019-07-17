let template_handler = (method, checkbox) => {
    let {checked, id} = checkbox;
    frappe.call({
        method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary." + method,
        args: {
            name: id,
            relevant: checked ? 1 : 0,
        },
        callback: r => {
            let {date, check} = r.message;
            $('.rel_label_' + id)[0].innerHTML = "&nbsp;&nbsp;" + date;

            let row_index = parseInt(checkbox.dataset.index);
            let row = frappe.query_report.datatable.datamanager.getRow(row_index);
            row[2].content = `${date};${check ? '1' : '0'};1`;
            frappe.query_report.datatable.datamanager.updateRow(row, row_index);
        }
    });
};

let mmic_dept_head_handler = (o) => {
    return template_handler("set_dept_head_relevant", o)
};

let rnd_spec_handler = (o) => {
    return template_handler("set_rnd_spec_relevant", o)
};

let developer_handler = (o) => {
    return template_handler("set_developer_relevant", o)
};

let opcon_spec_handler = (o) => {
    return template_handler("set_opcon_relevant", o)
};

let procmap_spec_handler = (o) => {
    return template_handler("set_procmap_relevant", o)
};

let desdoc_spec_handler = (o) => {
    return template_handler("set_desdoc_relevant", o)
};

let tech_writer_handler = (o) => {
    return template_handler("set_tech_writer_relevant", o)
};
