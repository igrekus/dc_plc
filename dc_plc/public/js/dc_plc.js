(function () {

	frappe.provide('frappe.dc_plc.utils');
	frappe.provide('frappe.dc_plc.utils.handlers');
	frappe.provide('frappe.dc_plc.utils.formatters');
	frappe.provide('frappe.dc_plc.utils.ui');

	frappe.require('assets/dc_plc/js/utils/formatter.js', () => {
		frappe.dc_plc.utils.formatters.mmic_dept_head_formatter = mmic_dept_head_formatter;
		frappe.dc_plc.utils.formatters.rnd_spec_formatter = rnd_spec_formatter;
		frappe.dc_plc.utils.formatters.developer_formatter = developer_formatter;
		frappe.dc_plc.utils.formatters.opcon_spec_formatter = opcon_spec_formatter;
		frappe.dc_plc.utils.formatters.procmap_spec_formatter = procmap_spec_formatter;
		frappe.dc_plc.utils.formatters.desdoc_spec_formatter = desdoc_spec_formatter;
		frappe.dc_plc.utils.formatters.tech_writer_formatter = tech_writer_formatter;

		frappe.dc_plc.utils.formatters.full_stat_formatter = full_stat_formatter;

		frappe.dc_plc.utils.formatters.function_link_formatter = function_link_formatter;
		frappe.dc_plc.utils.formatters.rnd_project_link_formatter = rnd_project_link_formatter;
		frappe.dc_plc.utils.formatters.product_type_link_formatter = product_type_link_formatter;
		frappe.dc_plc.utils.formatters.package_link_formatter = package_link_formatter;
		frappe.dc_plc.utils.formatters.letter_link_formatter = letter_link_formatter;
		frappe.dc_plc.utils.formatters.status_link_formatter = status_link_formatter;
		frappe.dc_plc.utils.formatters.step_link_formatter = step_link_formatter;
	});

	frappe.require('assets/dc_plc/js/utils/handler.js', () => {
		frappe.dc_plc.utils.handlers.mmic_dept_head_handler = mmic_dept_head_handler;
		frappe.dc_plc.utils.handlers.rnd_spec_handler = rnd_spec_handler;
		frappe.dc_plc.utils.handlers.developer_handler = developer_handler;
		frappe.dc_plc.utils.handlers.opcon_spec_handler = opcon_spec_handler;
		frappe.dc_plc.utils.handlers.procmap_spec_handler = procmap_spec_handler;
		frappe.dc_plc.utils.handlers.desdoc_spec_handler = desdoc_spec_handler;
		frappe.dc_plc.utils.handlers.tech_writer_handler = tech_writer_handler;
	});

	frappe.dc_plc.utils.replaceCharAt = (str, index, char) => {
		if (index > str.length - 1)
			return str;
		return str.substr(0, index) + char + str.substr(index + 1);
	};

	let value_or_none = value => {
		return value ? value : '-';
	};
	frappe.dc_plc.utils.value_or_none = value_or_none;

	let render_field_title = (frm, title, text) => {
		let field = frm.fields_dict[title];
		field.label_span.innerHTML = `${__(field._label)}&nbsp-&nbsp<b>${text}</b>`;
	};
	frappe.dc_plc.utils.ui.render_field_title = render_field_title;

	let render_info_field = (frm, field, label, content) => {
		frm.fields_dict[field].wrapper.innerHTML = `<span class="text-muted">${label}</span><br/><span>${content}</span>`;
	};
	frappe.dc_plc.utils.ui.render_info_field = render_info_field;

	frappe.dc_plc.utils.ui.set_field_title = (frm, title) => {
		if (!frm.fields_dict[title].value)
			return;
		frappe.db.get_doc(frm.fields_dict[title].df.options, frm.fields_dict[title].value).then(result => {
			render_field_title(frm, title, value_or_none(result.title));
		});
	};

	frappe.dc_plc.utils.ui.set_info_field = (frm, field, title) => {
		if (!frm.fields_dict[field].value)
			return;
		frappe.db.get_doc(frm.fields_dict[field].df.options, frm.fields_dict[field].value).then(result => {
			render_info_field(frm, field.replace('link_', 'info_'), title, value_or_none(result.title));
		});
	};

	setTimeout(() => { ELEMENT.locale(ELEMENT.lang.ruRU); }, 1000);
	console.log('>>> DC PLC init finished <<<');
})();
