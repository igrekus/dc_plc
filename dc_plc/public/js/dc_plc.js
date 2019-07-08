console.log(">>> DC PLC init <<<");

frappe.provide("frappe.dc_plc");

frappe.dc_plc.product_link_formatter = (value, row, column, row_data, format) => {
    if (!value) { value = '-'; }
    if (column.id === __('Relevance')) { return value; }
    return `<a href="http://${window.location.host}/desk#Form/DC_PLC_Product_Summary/${row_data.ID}">${value}</a>`;
};

// frappe.views.list_view["dc_list"] = new frappe.views.DCProductView();
