let template_handler = (method, checkbox) => {
    let {checked, id} = checkbox;
    let relevant = checked;
    let name = id;
    frappe.call({
        method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary." + method,
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
