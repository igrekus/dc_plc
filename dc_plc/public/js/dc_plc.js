(function () {

	frappe.provide('frappe.dc_plc.utils');
	frappe.provide('frappe.dc_plc.utils.handlers');
	frappe.provide('frappe.dc_plc.utils.formatters');

	frappe.require('assets/dc_plc/js/utils/formatter.js', () => {
		frappe.dc_plc.utils.product_link_formatter = product_link_formatter;

		frappe.dc_plc.utils.formatters.mmic_dept_head_formatter = mmic_dept_head_formatter;
		frappe.dc_plc.utils.formatters.rnd_spec_formatter = rnd_spec_formatter;
		frappe.dc_plc.utils.formatters.developer_formatter = developer_formatter;
		frappe.dc_plc.utils.formatters.opcon_spec_formatter = opcon_spec_formatter;
		frappe.dc_plc.utils.formatters.procmap_spec_formatter = procmap_spec_formatter;
		frappe.dc_plc.utils.formatters.desdoc_spec_formatter = desdoc_spec_formatter;
		frappe.dc_plc.utils.formatters.tech_writer_formatter = tech_writer_formatter;

		frappe.dc_plc.utils.function_link_formatter = function_link_formatter;
		frappe.dc_plc.utils.full_stat_formatter = full_stat_formatter;
		frappe.dc_plc.utils.rnd_project_link_formatter = rnd_project_link_formatter;
		frappe.dc_plc.utils.product_type_link_formatter = product_type_link_formatter;
		frappe.dc_plc.utils.package_link_formatter = package_link_formatter;
		frappe.dc_plc.utils.letter_link_formatter = letter_link_formatter;
		frappe.dc_plc.utils.status_link_formatter = status_link_formatter;
	});

	frappe.dc_plc.utils.handlers.mmic_dept_head_handler = (o) => {
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

	frappe.dc_plc.utils.handlers.rnd_spec_handler = (o) => {
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

	frappe.dc_plc.utils.handlers.developer_handler = (o) => {
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

	frappe.dc_plc.utils.handlers.opcon_spec_handler = (o) => {
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

	frappe.dc_plc.utils.handlers.procmap_spec_handler = (o) => {
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

	frappe.dc_plc.utils.handlers.desdoc_spec_handler = (o) => {
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

	frappe.dc_plc.utils.handlers.tech_writer_handler = (o) => {
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

	console.log('>>> DC PLC init finished <<<');
})();
