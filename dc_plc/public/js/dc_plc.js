console.log(">>> DC PLC init <<<");

frappe.provide("frappe.dc_plc");

frappe.dc_plc.product_link_formatter = (value, row, column, row_data, format) => {
    let new_value = '';

    if (!value) {
        return new_value;
    }
    if (column.id === __('Relevance')) {
        return value;
    }

    new_value = `<a href="http://${window.location.host}/desk#Form/DC_PLC_Product_Summary/${row_data.ID}">${value}</a>`;
    return new_value;
};

// frappe.views.list_view["dc_list"] = new frappe.views.DCProductView();
