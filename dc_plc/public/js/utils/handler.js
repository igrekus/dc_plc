let mmic_dept_head_handler = (o) => {
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

let rnd_spec_handler = (o) => {
    let relevant = o.checked;
    let name = o.id;
    frappe.call({
        method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary.set_rnd_spec_relevant",
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

let developer_handler = (o) => {
    let relevant = o.checked;
    let name = o.id;
    frappe.call({
        method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary.set_developer_relevant",
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

let opcon_spec_handler = (o) => {
    let relevant = o.checked;
    let name = o.id;
    frappe.call({
        method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary.set_opcon_relevant",
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


let procmap_spec_handler = (o) => {
    let relevant = o.checked;
    let name = o.id;
    frappe.call({
        method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary.set_procmap_relevant",
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

let desdoc_spec_handler = (o) => {
    let relevant = o.checked;
    let name = o.id;
    frappe.call({
        method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary.set_desdoc_relevant",
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

let tech_writer_handler = (o) => {
    let relevant = o.checked;
    let name = o.id;
    frappe.call({
        method: "dc_plc.dc_plc.doctype.dc_plc_product_summary.dc_plc_product_summary.set_tech_writer_relevant",
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
